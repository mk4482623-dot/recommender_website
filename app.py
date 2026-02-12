import streamlit as st
import pickle
import pandas as pd
import requests


@st.cache_data
def poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=d6998bc10599d29e9213e6c516a4672d&language=en-US"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get('poster_path'):
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"

    except requests.exceptions.RequestException:
        return "https://via.placeholder.com/500x750?text=No+Image"


def recommend(movie):
    recommended = []
    movie_poster = []
    matches = movies[movies['title_x']== movie]

    if matches.empty:
        st.error("Movie not found")
        return [], []
    index =matches.index[0]
    dist = similarity[index]
    mov_list = sorted(list(enumerate(dist)),reverse = True,key = lambda x:x[1])[1:7]

    for i in mov_list:
        movie_id = movies.iloc[i[0]].id
        recommended.append(movies.iloc[i[0]].title_x)
        movie_poster.append(poster(movie_id))
    return recommended , movie_poster

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similar.pkl', 'rb'))
st.title('Movie Recommendation System')

selected_movies = st.selectbox(
'what movie you choose!',
    movies['title_x'].values
)
if st.button("Recommend"):
    names,posters = recommend(selected_movies)
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