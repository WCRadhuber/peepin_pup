from flask import Blueprint, render_template
from peepin_pup.auth import login_required
bp = Blueprint('video', __name__)

@bp.route('/')
@login_required
def index():
    return render_template('video/index.html')
