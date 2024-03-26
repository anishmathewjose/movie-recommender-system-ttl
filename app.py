import streamlit as st
import pickle
import pandas as pd
import requests
from better_profanity import profanity 
import geocoder
from streamlit_card import card
import random

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id,st.secrets["TMDB"]))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x: x[1])[1:6]
    recommend_movies=[]
    recommend_movies_posters=[]
    for i in movie_list:
        movie_id= movies.iloc[i[0]].movie_id
        if profanity.contains_profanity(movies.iloc[i[0]].tags) and filterContent:
            recommend_movies.append('')
            recommend_movies_posters.append("https://via.placeholder.com/500x750?text=Adult+Content")
        else:
            recommend_movies.append(movies.iloc[i[0]].title)
            recommend_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommend_movies_posters

g = geocoder.ip('me')
def fetch_weather_conditions(latitude,longitude):
    response=requests.get('https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}'.format(latitude, longitude, st.secrets["OPENWEATHERMAP_APPID"]))
    data=response.json()
    return data['weather'][0]['main']
weather=fetch_weather_conditions(g.latlng[0], g.latlng[1])

weather_info={
    "Thunderstorm": ["Hear that rumble? It's the perfect night to curl up with a thrilling movie!", "https://images.unsplash.com/photo-1599070221195-bf2801877d7e?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", "thriller"],
    "Drizzle": ["Don't let the drizzle get you down! Brighten your day with a lighthearted family movie", "https://images.unsplash.com/photo-1541919329513-35f7af297129?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", "famili"],
    "Rain":["Feeling a bit gloomy with the rain? Brighten your day with a feel-good comedy movie","https://images.unsplash.com/photo-1493314894560-5c412a56c17c?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", "comedi"],
    "Snow":["It's snowing outside! How about curling up with a romantic movie?","https://images.unsplash.com/photo-1516715094483-75da7dee9758?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", "romanc"],
    "Clear":["Crystal clear skies tonight! Perfect for stargazing and a sci-fi adventure movie","https://images.unsplash.com/photo-1601297183305-6df142704ea2?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", "sciencefict"],
    "Clouds":["Cloudy skies got you feeling restless? Unleash some excitement with a pulse-pounding action movie","https://images.unsplash.com/photo-1525776759712-7b066ce45de0?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", "action"],
    "Mist":["The mist has rolled in, creating an eerie atmosphere! Why not settle in with a chilling mystery movie?","https://images.unsplash.com/photo-1515764371993-7995b2dba0b9?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", "mysteri"],
    "Smoke":["The smoky haze creates an eerie atmosphere. Perfect for a suspenseful horror movie","https://images.unsplash.com/36/STzPBJUsSza3mzUxiplj_DSC09775.JPG?q=80&w=2061&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", "horror"],
    "Haze":["The world's a bit blurry today. Escape into a lighthearted comedy movie and brighten your mood","https://images.unsplash.com/photo-1515764371993-7995b2dba0b9?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", "comedi"],
    "Dust":["The dust is swirling! Escape the dryness with a mind-bending sci-fi movie","https://images.unsplash.com/36/STzPBJUsSza3mzUxiplj_DSC09775.JPG?q=80&w=2061&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", "sciencefict"],
    "Fog":["Foggy weather can be spooky! How about a spine-tingling horror movie?", "https://images.unsplash.com/photo-1515764371993-7995b2dba0b9?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D","horror"],
    "Sand":["Sandstorm got you down? Seek shelter with a classic Film Noir full of mystery", "https://images.unsplash.com/36/STzPBJUsSza3mzUxiplj_DSC09775.JPG?q=80&w=2061&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D","mysteri"],
    "Ash":["Volcanic ash advisory! Stay safe indoors and escape into a thrilling sci-fi movie!", "https://images.unsplash.com/photo-1595347078352-d8d08c177040?q=80&w=1799&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D","sciencefict"],
    "Squall":["Looks like there's a squall outside! Stay safe indoors and curl up with a Thriller movie", "https://images.unsplash.com/photo-1641933002369-1122e78d0b47?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", "thriller"],
    "Tornado":["Looks like there's a tornado outside! Stay safe indoors and curl up with a Thriller movie","https://images.unsplash.com/photo-1641933002369-1122e78d0b47?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", "thriller"]
}

banner = card(
    title=weather_info[weather][0],
    text="",
    image=weather_info[weather][1],
    styles={
        "card": {
            "width": "100%",
            "height": "100px",
            "border-radius": "15px",
            "margin": "0px",
            "padding": "15vh"
        },
        "title": {
            "font-family": "'Tahoma', 'sans-serif'",
            "font-size": "17vh"
        }
    }
)

st.title('Movie Recommender System')
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movies["title"].values
)

filterContent=False
agefilter = st.checkbox('Enable PG-13 Filter')
if agefilter:
    filterContent=True

if st.button('Recommend'):
    names,posters = recommend(selected_movie)
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

if banner:
    filtered_movies = []
    for i in movies.iloc:
        if weather_info[weather][2] in i.tags:
            filtered_movies.append(i)
    random_movie = random.choice(filtered_movies)
    left_co1,left_co2, cent_co,last_co1,last_co2 = st.columns(5)
    with cent_co:
        st.text(random_movie.title)
        st.image(fetch_poster(random_movie.movie_id)) 
        st.caption("Perfect for today's weather")
