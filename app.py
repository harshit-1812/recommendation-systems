from urllib import response
import streamlit as st
import pandas as pd
import pickle
import requests

movie = pickle.load(open('movies.pkl','rb'))
#dict_ = pickle.load(open('dict.pkl','rb'))
#movies = pd.DataFrame(dict_)
movie_list = movie['title'].values
similarity = pickle.load(open('similarity.pkl','rb'))


def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=7e30525156e905a8dcaff7be94d0ba3a&language=en-US".format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie1):
    movie_index = int(movie[movie["title"]==movie1].index[0])
    distances = similarity[movie_index]
    recommendations = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies=[]
    recommended_movies_poster=[]
    for i in recommendations:
        movie_id = movie.iloc[i[0]].id
        recommended_movies.append(movie.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
   "Select a movie:",
   movie_list,
   index=None,
   placeholder="Select movie...",
)

st.write('You selected:', selected_movie_name)

if st.button("Recommend", type="primary"):
    try:
        names,posters = recommend(selected_movie_name)
        col1, col2, col3, col4,col5 = st.columns(5)

        with col1:
            st.image(posters[0])
            st.text(names[0])

        with col2:
            st.image(posters[1])
            st.text(names[1])

        with col3:
            st.image(posters[2])
            st.text(names[2])
            
        with col4:
            st.image(posters[3])
            st.text(names[3])
            
        with col5:
            st.image(posters[4])
            st.text(names[4])
    except:
        st.write("Select a movie first")