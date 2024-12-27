import io
import logging
from threading import Condition
from flask import Blueprint, render_template, Response
from peepin_pup.auth import login_required
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
bp = Blueprint('video', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        try:
            if buf.startswith(b'\xff\xd8'):
                # New frame, copy the existing buffer's content
                self.buffer.truncate()
                with self.condition:
                    self.frame = self.buffer.getvalue()
                    self.condition.notify_all()
                self.buffer.seek(0)
            return self.buffer.write(buf)
        except Exception as e:
            logger.error(f"Error writing frame: {e}")
            return 0

def gen_frames(output):
    """Generator function for streaming video frames."""
    try:
        while True:
            with output.condition:
                output.condition.wait()
                frame = output.frame
                if frame is None:
                    logger.warning("Empty frame recieved")
                    continue
            yield (b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except Exception as e:
        print(f"Error in frame generation: {str(e)}")

@bp.route('/feed')
@login_required
def video_feed():
    output = StreamingOutput()
    try:
        picam2.start_recording(JpegEncoder(), FileOutput(output))
        logger.info("Started video feed")
        return Response(gen_frames(output),
                       mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        logger.error(f"Error starting video feed {stir(e)}")
        return Response("Error starting video feed", status=500)

@bp.route('/')
@login_required
def index():
    return render_template('video/index.html')
