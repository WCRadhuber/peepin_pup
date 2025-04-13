from flask import Blueprint, stream_template, session, Response, stream_with_context
import requests
from peepin_pup.auth import login_required
bp = Blueprint('video', __name__)

@bp.route('/stream')
@login_required
def proxy_stream():
    stream_url = 'http://192.168.0.182:8000/stream.mjpg'

    def generate():
        with requests.get(stream_url, stream=True) as r:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    yield chunk

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=FRAME')

@bp.route('/')
@login_required
def index():
    return stream_template('video/index.html')
