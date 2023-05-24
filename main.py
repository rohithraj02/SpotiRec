import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import time
from model import *

def update_playlist_url():
    st.session_state.p_url = st.session_state.playlist_url

def playlist_page():
    st.subheader("User Playlist")
    st.markdown('---')
    playlist_uri = (st.session_state.playlist_url).split('/')[-1].split('?')[0]
    uri_link = 'https://open.spotify.com/embed/playlist/' + playlist_uri
    components.iframe(uri_link, height=500)
    return

def update_radio2():
    st.session_state.model=st.session_state.radio2

def update_radio1():
    st.session_state.model2 =st.session_state.radio1

def update_radio0():
    st.session_state.feature=st.session_state.radio

if 'radio' not in st.session_state:
    st.session_state.feature="Playlist"

if 'model' not in st.session_state:
    st.session_state.model = 'Model 1'

if 'p_url' not in st.session_state:
    st.session_state.p_url = 'Example: https://open.spotify.com/playlist/37i9dQZF1DX8FwnYE6PRvL?si=06ff6b38d4124af0'

def update_playlist_url():
    st.session_state.p_url = st.session_state.playlist_url

def rec_songs(recommended_playlist):
    track=recommended_playlist.track_id
    i=0
    for uri in track:
        # print(uri)
        uri_link = "https://open.spotify.com/embed/track/" + uri + "?utm_source=generator&theme=0"
        components.iframe(uri_link, height=80)
        i+=1
        if i%5==0:
            time.sleep(1)

def spr_sidebar():
    menu=option_menu(
        menu_title=None,
        options=['Home','About','Contact Us'],
        icons=['house','info-square','contact'],
        menu_icon='cast',
        default_index=0,
        orientation='horizontal'
    )
    if menu=='Home':
        st.session_state.app_mode = 'Home'
    elif menu=='Result':
        st.session_state.app_mode = 'Result'
    elif menu=='About':
        st.session_state.app_mode = 'About'
    elif menu=='Contact Us':
        st.session_state.app_mode = 'Contact Us'

def play_recomm():
    # connectToSpotify(st.session_state.playlist_url)
    with st.spinner('Getting Recommendations...'):
        recommended_playlist=read_Transform(st.session_state.playlist_url)
    # st.dataframe(recommended_playlist)
    st.header('Top 15 Recommended songs')
    rec_songs(recommended_playlist)
    
def home_page():
    st.session_state.radio=st.session_state.feature
    st.session_state.radio2=st.session_state.model

    st.title('SpotiRec')
    st.markdown('SpotiRec is a content-based music recommending system')
    # col,col2,col3=st.columns([2,2,3])
    # radio=col.radio("Feature",options=("Playlist","Song","Artist Top Tracks"),key='radio',on_change=update_radio0)
    # if radio =="Playlist" or radio =="Song" :
    #     radio2=col2.radio("Model",options=("Model 1","Model 2","Spotify Model"),key='radio2',on_change=update_radio2)

    
    

    st.session_state.playlist_url = st.session_state.p_url
    st.markdown("<br>", unsafe_allow_html=True)
    Url = st.text_input(label="Playlist Url",key='playlist_url',on_change=update_playlist_url)
                        # ,on_change=update_playlist_url
    with st.expander("Here's how to find any Playlist URL in Spotify"):
        st.write(""" 
        - Search for Playlist on the Spotify app
        - Right Click on the Playlist you like
        - Click "Share"
        - Choose "Copy link to playlist"
    """)
        st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    playlist_page()
    state =st.button('Get Recommendations')
    
        # st.image('spotify_get_playlist_url.png')
    if state:
        play_recomm()
    
# def result_page():
#     if 'rs' not in st.session_state:
#         st.error('Please select a model on the Home page and run Get Recommendations')
#     else:
#         st.success('Top {} recommendations'.format(len(st.session_state.rs)))
#         i=0
#         for uri in st.session_state.rs:
#          uri_link = "https://open.spotify.com/embed/track/" + uri + "?utm_source=generator&theme=0"
#          components.iframe(uri_link, height=80)
#          i+=1
#          if i%5==0:
#             time.sleep(1)
# def Log_page():
#     log=st.checkbox('Display Output', True, key='display_output')
#     if log == True:
#      if 'err' in st.session_state:
#         st.write(st.session_state.err)
#     with open('Data/streamlit.csv') as f:
#         st.download_button('Download Dataset', f,file_name='streamlit.csv')

def About_page():
    st.header('Development')
    """
    Check out the [repository](https://github.com/abdelrhmanelruby/Spotify-Recommendation-System) for the source code and approaches, and don't hesitate to contact me if you have any questions. I'm excited to read your review.
    [Github](https://github.com/abdelrhmanelruby)  [Linkedin](https://www.linkedin.com/in/abdelrhmanelruby/) Email : abdelrhmanelruby@gmail.com
    """
    st.subheader('Spotify Million Playlist Dataset')
    """
    For this project, I'm using the Million Playlist Dataset, which, as its name implies, consists of one million playlists.
    contains a number of songs, and some metadata is included as well, such as the name of the playlist, duration, number of songs, number of artists, etc.
    """

    """
    It is created by sampling playlists from the billions of playlists that Spotify users have created over the years. 
    Playlists that meet the following criteria were selected at random:
    - Created by a user that resides in the United States and is at least 13 years old
    - Was a public playlist at the time the MPD was generated
    - Contains at least 5 tracks
    - Contains no more than 250 tracks
    - Contains at least 3 unique artists
    - Contains at least 2 unique albums
    - Has no local tracks (local tracks are non-Spotify tracks that a user has on their local device
    - Has at least one follower (not including the creator
    - Was created after January 1, 2010 and before December 1, 2017
    - Does not have an offensive title
    - Does not have an adult-oriented title if the playlist was created by a user under 18 years of age
    Information about the Dataset [here](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge)
    """
    st.subheader('Audio Features Explanation')
    """
    | Variable | Description |
    | :----: | :---: |
    | Acousticness | A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic. |
    | Danceability | Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable. |
    | Energy | Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy. |
    | Instrumentalness | Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0. |
    | Key | The key the track is in. Integers map to pitches using standard Pitch Class notation. E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on. If no key was detected, the value is -1. |
    | Liveness | Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live. |
    | Loudness | The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typically range between -60 and 0 db. |
    | Mode | Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0. |
    | Speechiness | Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks. |
    | Tempo | The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration. |
    | Time Signature | An estimated time signature. The time signature (meter) is a notational convention to specify how many beats are in each bar (or measure). The time signature ranges from 3 to 7 indicating time signatures of "3/4", to "7/4". |
    | Valence | A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry). |
    
    Information about features: [here](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features)
    """

def Contact():
    st.header('call Punith the boSS at +91 73381 35131')
    st.header('Address: ')
    st.markdown('Number 23, 2nd Main, 3rd Cross \n Balaji Nagar, Bangalore')
    # st.markdown("<br>", unsafe_allow_html=True)
    # st.subheader('Balaji Nagar, Bangalore')


def main():
    spr_sidebar()        
    if st.session_state.app_mode == 'Home':
        home_page()
    # if st.session_state.app_mode == 'Result':
    #     result_page()
    if st.session_state.app_mode == 'About' :
        About_page()
    if st.session_state.app_mode == 'Contact Us':
        Contact()
# Run main()
if __name__ == '__main__':
    main()