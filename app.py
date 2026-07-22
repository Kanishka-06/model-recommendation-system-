import pickle
import streamlit as st
import requests
from sklearn.metrics.pairwise import cosine_similarity

# def fetch_poster(movie_id):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
#     data = requests.get(url)
#     data = data.json()
#     poster_path = data['poster_path']
#     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#     return full_path

def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"

    response = requests.get(url)

    if response.status_code != 200:
        return ""

    data = response.json()

    poster_path = data.get("poster_path")

    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path

    return ""


def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]

    movie_vector = vectors[movie_index]

    distances = cosine_similarity(movie_vector, vectors).flatten()

    movies_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    recommended_movies = []
    recommended_movie_posters = []

    for i in movies_list:

        movie = movies.iloc[i[0]]

        movie_id = movie["id"]

        recommended_movies.append(movie["title"])

        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movie_posters
# def recommend(movie):
#     index = movies[movies['title'] == movie].index[0]
#     distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
#     recommended_movie_names = []
#     recommended_movie_posters = []
#     for i in distances[1:6]:
#         # fetch the movie poster
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_movie_posters.append(fetch_poster(movie_id))
#         recommended_movie_names.append(movies.iloc[i[0]].title)

#     return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
# movies = pickle.load(open('movie_list.pkl','rb'))
# st.write(movies.columns)
# st.write(movies.head())
movies = pickle.load(open('movie_list.pkl','rb'))
# similarity = pickle.load(open('model/similarity.pkl','rb'))
vectors = pickle.load(open('vectors.pkl','rb'))
vectorizer = pickle.load(open('vectorizer.pkl','rb'))


movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)



# if st.button('Show Recommendation'):
#     recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
if st.button('Show Recommendation'):

    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    if len(recommended_movie_names) < 5:
        st.error("Could not generate 5 recommendations.")
        st.stop()
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])



