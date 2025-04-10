import streamlit as st
import pickle #for file copy
import pandas as pd
import numpy as np
import requests  #for poster



#file copied from model.ipynb
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity= pickle.load(open('similarity.pkl', 'rb'))
movies=pd.DataFrame(movies_dict)  #movies inplace of new_df


#poster function
def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

    

#recommend function
def recommend(movie):
    movie_index= movies[movies['title']==movie]. index[0]  #index 0 means for first movie AVATAR
    distances= similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]  # over here its distances and  not similarity
    
    recommended_movies=[]
    recommended_posters=[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id  
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))   #fetch poster from API
    return recommended_movies, recommended_posters


#MAIN
st.title("🎬 Movie Recommender System")

option = st.selectbox(
    "SELECT A MOVIE U WANNA WATCH",
    (movies['title'].values),
)
st.write("You selected:", option)

if st.button("Recommend"):
    names,posters=recommend(option)
    
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
        
   
# BACKGROUND IMAGE     
import base64

def set_bg_from_url(url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )   
    
set_bg_from_url("https://i.pinimg.com/736x/1c/31/26/1c31267d467803d3845a09f7c5c626fd.jpg")
