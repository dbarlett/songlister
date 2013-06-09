from flask import render_template
from app import app, models


@app.route('/')
@app.route('/index')
def index():
    u = models.User.query.filter_by(id=2).first()
    user_songs = u.songs
    all_songs = models.Song.query.all()
    return render_template(
        "index.html",
        user_songs=user_songs,
        all_songs=all_songs
    )