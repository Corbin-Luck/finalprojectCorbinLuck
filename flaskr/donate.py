### INF601 - Advanced Programming in Python
### Corbin Luck
### Final Project

from flask import Blueprint, render_template

bp = Blueprint('donate', __name__)

@bp.route('/donate')
def donate():
    return render_template('donate.html')