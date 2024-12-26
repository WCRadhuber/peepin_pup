import io
from threading import Condition
from flask import Blueprint, render_template, Response
from peepin_pup.auth import login_required
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
bp = Blueprint('video', __name__)



class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

def gen_frames(output):
    """Generator function for streaming video frames."""
    try:
        while True:
            with output.condition:
                output.condition.wait()
                frame = output.frame
            yield (b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except Exception as e:
        print(f"Error in frame generation: {str(e)}")

@bp.route('/feed')
@login_required
def video_feed():
    output = StreamingOutput()
    picam2.start_recording(JpegEncoder(), FileOutput(output))
    return Response(gen_frames(output),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@bp.route('/')
@login_required
def index():
    return render_template('video/index.html')
