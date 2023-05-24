import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util

from skimage import io
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

def read_Transform(playlist_link):
    # print('hi')
    spotify_data = pd.read_csv('SpotifyFeatures.csv')
    # spotify_data.head()

    spotify_features_df = spotify_data
    genre_OHE = pd.get_dummies(spotify_features_df.genre)
    key_OHE = pd.get_dummies(spotify_features_df.key)

    scaled_features = MinMaxScaler().fit_transform([
    spotify_features_df['acousticness'].values,
    spotify_features_df['danceability'].values,
    spotify_features_df['duration_ms'].values,
    spotify_features_df['energy'].values,
    spotify_features_df['instrumentalness'].values,
    spotify_features_df['liveness'].values,
    spotify_features_df['loudness'].values,
    spotify_features_df['speechiness'].values,
    spotify_features_df['tempo'].values,
    spotify_features_df['valence'].values,
    ])

    spotify_features_df[['acousticness','danceability','duration_ms','energy','instrumentalness','liveness','loudness','speechiness','tempo','valence']] = scaled_features.T

    spotify_features_df = spotify_features_df.drop('genre',axis = 1)
    spotify_features_df = spotify_features_df.drop('artist_name', axis = 1)
    spotify_features_df = spotify_features_df.drop('track_name', axis = 1)
    spotify_features_df = spotify_features_df.drop('popularity',axis = 1)
    spotify_features_df = spotify_features_df.drop('key', axis = 1)
    spotify_features_df = spotify_features_df.drop('mode', axis = 1)
    spotify_features_df = spotify_features_df.drop('time_signature', axis = 1)

    spotify_features_df = spotify_features_df.join(genre_OHE)
    spotify_features_df = spotify_features_df.join(key_OHE)
    # print('spotify data')
    # print(spotify_data)
    # spotify_features_df.head()
    playlist_df=connectToSpotify(playlist_link,spotify_data)
    playlist_vector, nonplaylist_df = generate_playlist_vector(spotify_features_df, playlist_df, 1.2)
    top15 = generate_recommendation(spotify_data, playlist_vector, nonplaylist_df)  
    return(top15)

def connectToSpotify(playlist_link,spotify_data):
    client_id='f4bedc5ed9b5474385de479c1e8eebd2'
    client_secret='1626ff5a29ee4c00b7ecb38179d64ffd'
    scope = 'user-library-read'
    token = util.prompt_for_user_token(
        scope, 
        client_id= client_id, 
        client_secret=client_secret, 
        redirect_uri='http://localhost:8881/callback'
  )
    sp = spotipy.Spotify(auth=token)
    # playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f"
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]
    # print(track_uris)
    playlist = pd.DataFrame()
    i=0
    for track in sp.playlist_tracks(playlist_URI)["items"]:
        #URI
        track_uri = track["track"]["uri"]
        
        #Track name
        playlist.loc[i, 'artist'] = track["track"]["artists"][0]["name"]
        playlist.loc[i, 'track_name']= track["track"]["name"]
        playlist.loc[i, 'track_id']=track["track"]["id"]
        playlist.loc[i, 'url']=track['track']['album']['images'][1]['url']
        playlist.loc[i, 'date_added'] = track['added_at']
        # print(track_name) 
        #Main Artist
        artist_uri = track["track"]["artists"][0]["uri"]
        artist_info = sp.artist(artist_uri)
        
        #Name, popularity, genre
        artist_pop = artist_info["popularity"]
        artist_genres = artist_info["genres"]
        
        #Album
        album = track["track"]["album"]["name"]
        
        #Popularity of the track
        track_pop = track["track"]["popularity"]
        i+=1

    playlist['date_added'] = pd.to_datetime(playlist['date_added'])  
    playlist = playlist[playlist['track_id'].isin(spotify_data['track_id'].values)].sort_values('date_added',ascending = False)
    return(playlist)

def generate_playlist_vector(spotify_features, playlist_df, weight_factor):
    
    spotify_features_playlist = spotify_features[spotify_features['track_id'].isin(playlist_df['track_id'].values)]
    spotify_features_playlist = spotify_features_playlist.merge(playlist_df[['track_id','date_added']], on = 'track_id', how = 'inner')
    
    spotify_features_nonplaylist = spotify_features[~spotify_features['track_id'].isin(playlist_df['track_id'].values)]
    
    playlist_feature_set = spotify_features_playlist.sort_values('date_added',ascending=False)
    
    
    most_recent_date = playlist_feature_set.iloc[0,-1]
    
    for ix, row in playlist_feature_set.iterrows():
        playlist_feature_set.loc[ix,'days_from_recent'] = int((most_recent_date.to_pydatetime() - row.iloc[-1].to_pydatetime()).days)
        
    
    playlist_feature_set['weight'] = playlist_feature_set['days_from_recent'].apply(lambda x: weight_factor ** (-x))
    
    playlist_feature_set_weighted = playlist_feature_set.copy()
    
    playlist_feature_set_weighted.update(playlist_feature_set_weighted.iloc[:,:-3].mul(playlist_feature_set_weighted.weight.astype(int),0))   
    
    playlist_feature_set_weighted_final = playlist_feature_set_weighted.iloc[:, :-3]
    

    
    return playlist_feature_set_weighted_final.sum(axis = 0), spotify_features_nonplaylist

def generate_recommendation(spotify_data, playlist_vector, nonplaylist_df):

    non_playlist = spotify_data[spotify_data['track_id'].isin(nonplaylist_df['track_id'].values)]
    non_playlist['sim'] = cosine_similarity(nonplaylist_df.drop(['track_id'], axis = 1).values, playlist_vector.drop(labels = 'track_id').values.reshape(1, -1))[:,0]
    non_playlist_top15 = non_playlist.sort_values('sim',ascending = False).head(15)
    # non_playlist_top15['url'] = non_playlist_top15['track_id'].apply(lambda x: sp.track(x)['album']['images'][1]['url'])
    
    return  non_playlist_top15

# connectToSpotify('https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f')
read_Transform('https://open.spotify.com/playlist/5VZ6xxArnfM07J09jP4dTJ?si=82db568f7c114664')