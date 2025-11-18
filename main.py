from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
import requests
from dotenv import load_dotenv
import os

load_dotenv()
key = os.environ.get('FLASK_KEY')
#this key can be whatever you want, but you have to set for the code to run

class MovieForm(FlaskForm):
    rating = FloatField("Your Rating Out of 10 e.g. 8.5" , validators = [DataRequired()])
    review  = StringField("Your Review", validators=[DataRequired()])
    submit = SubmitField(label="Done", render_kw={'class': 'btn btn-light mt-3'})

class AddForm(FlaskForm):
    title = StringField("Movie Title",validators=[DataRequired()])
    submit = SubmitField(label = "Add Movie", render_kw ={'class': 'btn btn-light mt-3'})

def add_movie(new_movie):
    with app.app_context():
        db.session.add(new_movie)
        db.session.commit()

def get_movies():
    with app.app_context():
        result = db.session.execute(db.select(Movie).order_by(Movie.rating.desc()))
        all_movies = result.scalars().all()
        count = 1
        for movie in all_movies:
            movie.ranking = count
            count += 1
        result = db.session.execute(db.select(Movie).order_by(Movie.ranking))
        all_movies = result.scalars().all()
        return all_movies

def get_movie_by_id(id):
    with app.app_context():
        movie = db.session.execute(db.select(Movie).where(Movie.id == id)).scalar()
        return movie

def get_movie_by_title(title):
    with app.app_context():
        movie = db.session.execute(db.select(Movie).where(Movie.title == title)).scalar()
        return movie

def delete_movie_by_id(id):
    with app.app_context():
        book_to_delete = db.session.execute(db.select(Movie).where(Movie.id == id)).scalar()
        db.session.delete(book_to_delete)
        db.session.commit()

def update_rating_review(new_rating,new_review,id):
    with app.app_context():
        movie_to_update = db.session.execute(db.select(Movie).where(Movie.id == id)).scalar()
        movie_to_update.rating = new_rating
        movie_to_update.review = new_review
        db.session.commit()

app = Flask(__name__)
app.config['SECRET_KEY'] = key
Bootstrap5(app)

url = "https://api.themoviedb.org/3/search/movie?query="
url_details = "https://api.themoviedb.org/3/movie/"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1ZTYyNmExNTNjYWYwMDQzMzE1NGI5MmYwZjM2OGQ3MCIsIm5iZiI6MTc2MTkzODg4NC43NTksInN1YiI6IjY5MDUwZGM0ODFkMDI1MDJmODJmZGZjMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.ggpcYCdyYj09oH4I6zOrvS8g2itZt2RswwuX7WqZ41A"
}


# CREATE DB

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///movie-collection.db"
db =SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique = True)
    year: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String(400))
    rating: Mapped[float] = mapped_column(Float)
    ranking: Mapped[int] = mapped_column(Integer)
    review: Mapped[str] = mapped_column(String(400))
    img_url: Mapped[str] = mapped_column(String(100))

    def __repr__(self):
        return f'<Movie {self.title}>'

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html", movies = get_movies())

@app.route("/edit/<id>", methods = ['GET', 'POST'])
def edit_movie(id):
    form = MovieForm()
    if form.validate_on_submit():
        update_rating_review( form.rating.data , form.review.data, id)
        return redirect(url_for('home'))
    return render_template('edit.html', form=form)

@app.route("/delete/<id>")
def delete_movie(id):
    delete_movie_by_id(id)
    return redirect(url_for('home'))

@app.route("/add", methods=['GET','POST'])
def add():
    form = AddForm()
    if form.validate_on_submit():
        title = form.title.data
        response = requests.get(f"{url}{title}", headers=headers)
        return render_template('select.html', data = response.json())
    return render_template('add.html', form = form)

@app.route("/get_added/<index>")
def add_mov(index):
    response = requests.get(f"{url_details}{index}",headers=headers)
    data = response.json()
    m = Movie(
        title = data["original_title"],
        year = data["release_date"].split("-")[0],
        description =data["overview"],
        img_url = f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
        rating = 0,
        ranking = 0,
        review = "-"
    )
    add_movie(m)
    return redirect(url_for('edit_movie', id = get_movie_by_title( data["original_title"]).id ))


if __name__ == '__main__':
    app.run(debug=True)


