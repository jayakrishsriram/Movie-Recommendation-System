from imdb import IMDb
import streamlit as st
import pandas as pd
import requests
import pickle

# Function to retrieve movie poster by movie name
def get_movie_poster(movie_name):
    ia = IMDb()
    # Search for the movie by name
    search_results = ia.search_movie(movie_name)
    
    if search_results:
        # Get the first result (most relevant)
        movie = search_results[0]
        ia.update(movie)  # Fetch additional details

        # Get the IMDb ID and movie title
        title = movie['title']

        # Get the poster URL (if available)
        poster_url = movie.get('full-size cover url')

        # Print the result
        if poster_url:
            return poster_url
        else:
            print(f"No poster found for '{title}'")


# Streamlit app title
st.title("Movie Recommendation System")

# Sidebar for settings
st.sidebar.header("Settings")

# Option to choose between PG-13, R-Rated, and All
rating_option = st.sidebar.radio(
    "Choose Movie Rating",
    ("All","PG-13")
)


# Load the processed data and similarity matrix
with open('movie_data.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file)

df=pd.read_csv('Modified_data.csv')
# Function to get movie recommendations
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Get top 10 similar movies
    movie_indices = [i[0] for i in sim_scores]
    return movies[['title', 'movie_id']].iloc[movie_indices]
def call(data):
    selected_movie = st.selectbox("Select a movie:", data['title'].values)

    if st.button('Recommend'):
        recommendations = get_recommendations(selected_movie)
        st.write("Top 10 recommended movies:")

        # Create a 2x5 grid layout
        for i in range(0, 10, 5):  # Loop over rows (2 rows, 5 movies each)
            cols = st.columns(5)  # Create 5 columns for each row
            for col, j in zip(cols, range(i, i+5)):
                if j < len(recommendations):
                    movie_title = recommendations.iloc[j]['title']
                    poster_url = get_movie_poster(movie_title)
                    with col:
                        st.image(poster_url, width=130)
                        st.write(movie_title)
# Function for PG-13 movies
def pg13_movies():
    data=df[df['adult']==False]
    call(data)


# Function for All movies
def all_movies():
    call(df)


# Execute different functions based on the selected rating
if rating_option == "PG-13":
    pg13_movies()
else:
    all_movies()

