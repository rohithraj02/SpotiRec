import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import time
from model import *
from PIL import Image


def update_playlist_url():
    st.session_state.p_url = st.session_state.playlist_url

def playlist_page():
    st.subheader("User Playlist")
    st.markdown('---')
    playlist_uri = (st.session_state.playlist_url).split('/')[-1].split('?')[0]
    uri_link = 'https://open.spotify.com/embed/playlist/' + playlist_uri
    components.iframe(uri_link, height=500)
    return


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

def menu_bar():
    menu=option_menu(
        menu_title=None,
        options=['Home','Top global','About','Contact Us'],
        icons=['house','music-note-beamed','info-square','contact'],
        menu_icon='cast',
        default_index=0,
        orientation='horizontal'
    )
    if menu=='Home':
        st.session_state.app_mode = 'Home'
    elif menu=='Top global':
        st.session_state.app_mode = 'Top global'
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

    st.title('SpotiRec')
    st.markdown('SpotiRec is a content-based music recommending system')
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
    


def About_page():
    cosine_sim=Image.open('Cosine_similarity.png')
    st.header('How the recommendation system works')

    """
    Content-based filtering system: Content-Based recommender system tries to guess the features or behavior of a user given the item’s features, he/she reacts positively to.
    Once, we know the likings of the user we can embed the features in an embedding space using the feature vector generated and recommend songs to them according to their liking. During recommendation, the similarity metrics (Cosine Similarity) are calculated from the item’s feature vectors and the user’s preferred feature vectors from his/her previous records. Then, the top few are recommended.
    """
    # st.subheader('Audio Features Explanation')
    """
    Information about audio features: [here](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features)    
    """
    st.subheader('Cosine Similarity')
    """
    Cosine similarity is a metric used to measure how similar the documents are irrespective of their size. Mathematically, it measures the cosine of the angle between two vectors projected in a multi-dimensional space.
    The cosine similarity is advantageous because even if the two similar documents are far apart by the Euclidean distance (due to the size of the document), chances are they may still be oriented closer together. The smaller the angle, higher the cosine similarity.
    """
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(' ')

    with col2:
        st.image(cosine_sim, caption='Cosine Similarity')

    with col3:
        st.write(' ')

def Contact():
    st.header('Project by Rohith Rajendran and Punith C')
    st.subheader('email id:')
    """
    rohithraj2015@gmail.com\n
    punithshetty408@gmail.com
    """
    st.header('GitHub repo:')
    """
    [https://github.com/rohithraj02/SpotiRec](https://github.com/rohithraj02/SpotiRec)
    """
    # st.header('Address: ')
    # st.markdown('Number 23, 2nd Main, 3rd Cross \n Balaji Nagar, Bangalore')
    # st.markdown("<br>", unsafe_allow_html=True)
    # st.subheader('Balaji Nagar, Bangalore')
def Top_global():
    uri_link = 'https://open.spotify.com/embed/playlist/37i9dQZEVXbNG2KDcFcKOF?si=2d52bb14f33c459b'
    components.iframe(uri_link, height=500)
    return

def main():
    menu_bar()        
    if st.session_state.app_mode == 'Home':
        home_page()
    if st.session_state.app_mode == 'Top global':
        Top_global()
    if st.session_state.app_mode == 'About' :
        About_page()
    if st.session_state.app_mode == 'Contact Us':
        Contact()
    
# Run main()
if __name__ == '__main__':
    main()