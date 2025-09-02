import streamlit as st
import pickle
import pandas as pd
import requests
from streamlit_extras.let_it_rain import rain

st.set_page_config(layout="wide")

with st.container(horizontal=True, horizontal_alignment="right", width="stretch"):
    st.title('Movie Review and Recommendation System')

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))


def recommend(movie):
    # original movie details
    movie_index = movies[movies['title'] == movie].index[0]
    movie_list = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:6]
    main_movie_id = int(movies[movies['title'] == movie]['id'].to_dict()[movie_index])
    main_response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=7ddc9a2d0d3d38d110ba4bf667bb1315'.format(main_movie_id),
        proxies={"http": None, "https": None})
    main_data = main_response.json()
    main_image = ('https://image.tmdb.org/t/p/w342/{}'.format(main_data['poster_path']))
    main_link = main_data['homepage']
    st.write("")

    # Original movie expander box
    with st.expander("See movie details"):
        colA, colB = st.columns(2)
        with colA:
            st.image(main_image, width='content')

        with colB:
            st.subheader(movie)
            st.caption('- ' + main_data['tagline'])
            st.divider()
            st.write('- Overview')
            st.caption(main_data['overview'])
            st.divider()
            st.write("- Average Rating:  "+str(main_data['vote_average'])+'/10')
            st.divider()
            st.link_button('Click for homepage', main_link, icon="🎞️")

    # code for recommendations
    dict = {}
    for i in movie_list:
        movie_name = movies.iloc[i[0]].title
        movie_id = int(movies[movies['title'] == movie_name]['id'].to_dict()[i[0]])
        response = requests.get(
            'https://api.themoviedb.org/3/movie/{}?api_key=7ddc9a2d0d3d38d110ba4bf667bb1315'.format(movie_id),
            proxies={"http": None, "https": None}
        )
        data = response.json()
        image = ('https://image.tmdb.org/t/p/original/{}'.format(data['poster_path']))
        link = data['homepage']
        dict[movie_name] = [image, link]

    st.write('')
    st.badge("More movies to watch...", color='green')
    st.write("")

    col1, col2, col3, col4, col5 = st.columns(5, gap='small', vertical_alignment='bottom')
    cols = [col1, col2, col3, col4, col5]
    titles = list(dict.keys())
    posters = list(dict.values())

    for col, title, poster in zip(cols, titles, posters):
        with col:
            st.subheader(title)
            st.image(poster[0], width='stretch')
            st.link_button('Go to movie Homepage', poster[1], icon="🎞️")
    rain(
        emoji="❄️",
        font_size=25,
        falling_speed=10,
        animation_length="6",
    )



option = st.selectbox('Select a movie', movies['title'].values)

if st.button('Recommend', type='primary'):
    recommend(option)
