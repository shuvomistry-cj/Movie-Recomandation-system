import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster using TMDB API
def fetch_poster(movie_id):
    api_key = '11113a6e1932a3a38aee76c985278e7f'
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US')
    data = response.json()
    if 'poster_path' in data and data['poster_path']:
        return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# Function to recommend movies
def recommend(movie, movies):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id  # Use movie ID to fetch poster
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Load the movies data from pickle file
with open('moviesdict.pkl', 'rb') as file:
    movies_dict = pickle.load(file)

# Convert the dictionary into a pandas DataFrame
movies = pd.DataFrame(movies_dict)

# Load the similarity data from pickle file
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI setup
st.title('Movie Recommender System')

# Dropdown to select a movie
selected_movie_name = st.selectbox(
    "Select a Movie",
    movies['title'].values
)

# Button to get recommendations
if st.button("Recommend"):
    names, posters = recommend(selected_movie_name, movies)

    # Display recommended movies in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
