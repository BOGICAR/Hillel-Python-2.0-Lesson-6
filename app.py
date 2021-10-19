from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    pk = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    info = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    actor_pk = db.Column(db.Integer, db.ForeignKey('actor.pk'), nullable=False)
    actor = db.relationship('Actor', backref=db.backref('movies', lazy=True))

    genre_pk = db.Column(db.Integer, db.ForeignKey('genre.pk'), nullable=False)
    genre = db.relationship('Genre', backref=db.backref('movies', lazy=True))


    def __repr__(self):
        return '<Movie %r>' % self.pk


class Actor(db.Model):
    pk = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    info = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Actor %r>' % self.pk

class Genre(db.Model):
    pk = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(100), nullable=False)
    info = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Genre %r>' % self.pk


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/movies')
def movies():
    movies = Movie.query.order_by(Movie.date.desc()).all()
    return render_template('movies.html', movies=movies)


@app.route('/movies/<int:pk>')
def movie_detail(pk):
    movie = Movie.query.get(pk)
    return render_template('movie_detail.html', movie=movie)


@app.route('/create-movie', methods=['POST', 'GET'])
def create_movie():
    if request.method == 'POST':
        name = request.form['name']
        info = request.form['info']

        movie = Movie(name=name, info=info)

        try:
            db.session.add(movie)
            db.session.commit()
            return redirect('/movies')
        except:
            return 'При добавлении фильма произошла ошибка'
    else:
        return render_template('create-movie.html')


if __name__ == '__main__':
    app.run(debug=True)
