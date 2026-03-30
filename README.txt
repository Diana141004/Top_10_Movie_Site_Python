# 🎬 Top 10 Movie Collection Manager

## 📖 Overview
Welcome to my personalized Movie Ranking Web App! This is one of my first major steps into Python web development. 

This application allows you to curate a list of your all-time favorite movies. Instead of manually typing out movie details, the app integrates with the **TMDB (The Movie Database) API** to instantly fetch movie titles, release years, descriptions, and official poster images. You simply search for a movie, add it, give it your personal rating, and the app automatically re-calculates the ranking of all movies in your database.

## ✨ Key Features
* **Smart Search:** Search for any movie using the TMDB API integration.
* **Auto-Sorting Ranking:** Whenever you add a new movie or update an existing rating, the application automatically dynamically re-sorts and updates the rank (1 to 10) of every movie in your collection.
* **Full CRUD Functionality:** * **C**reate: Add new movies to your list.
  * **R**ead: View your beautiful movie cards with real posters on the home page.
  * **U**pdate: Modify your personal rating and review text at any time.
  * **D**elete: Remove a movie from your list if it no longer makes the cut.

## 🛠️ Tech Stack
* **Backend:** Python, Flask
* **Database:** SQLite, Flask-SQLAlchemy (ORM)
* **Frontend:** HTML, Bootstrap 5 (via Flask-Bootstrap)
* **Forms & Validation:** Flask-WTF, WTForms
* **APIs:** TMDB API (Requests library)

---

## 🚀 Getting Started

To run this application locally, follow these steps:

### 1. Prerequisites
Ensure you have Python installed. Then, install the required dependencies:
`pip install Flask Flask-Bootstrap Flask-SQLAlchemy Flask-WTF requests python-dotenv`

### 2. API Key Setup
You will need a free API key from The Movie Database.
1. Create an account at [TMDB](https://www.themoviedb.org/).
2. Go to your account settings, navigate to the API section, and request an API key/Read Access Token.

### 3. Environment Variables
Create a `.env` file in the root directory of the project and add your secret keys. 

FLASK_KEY=your_random_secret_key_here
TMDB_TOKEN=your_tmdb_read_access_token_here
AUTHORIZATION = your_authorization_token_here

### 4. Run the Application
Start the Flask server:
`python main.py`

Open your web browser and go to `http://127.0.0.1:5000` to start building your movie collection!

---
*Note: The SQLite database (`movie-collection.db`) is generated automatically the first time you run the app.*
