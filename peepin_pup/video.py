import os
from flask import Blueprint, stream_template, Response, stream_with_context
import requests
from peepin_pup.auth import login_required
bp = Blueprint('video', __name__)

camera_streams = eval(os.environ.get('STREAMS'))


@bp.route('/stream/<int:camera_id>')
@login_required
def proxy_stream(camera_id):

    stream_url = camera_streams.get(camera_id)

    if not stream_url:
        return "Camera not found", 404

    def generate():
        with requests.get(stream_url, stream=True) as r:
            if r.status_code != 200:
                yield b'--FRAME\r\nContent-Type: text/plain\r\n\r\nStream unavailable\r\n\r\n'
                return
            for chunk in r.iter_content(chunk_size=4096):
                if chunk:
                    yield chunk

    return Response(stream_with_context(generate()), mimetype='multipart/x-mixed-replace; boundary=FRAME')


@bp.route('/')
@login_required
def index():
    return stream_template('video/index.html', camera_ids=camera_streams.keys())
