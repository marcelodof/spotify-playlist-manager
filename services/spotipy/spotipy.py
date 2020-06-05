"""Spotipy Class."""
import spotipy
import spotipy.util as util
import pandas as pd
import time


class Spotipy():
    """Spotipy Class Main Entry Point."""
    def __init__(self, configs):
        """Spotipy Init."""
        self.configs = configs
        self.get_authorization()
        self.batch_limit = 100
        self.columns = [
            "id",
            "name",
            "artist",
            "popularity",
            "key",
            "energy",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "valence",
            "tempo"
        ]

    def get_authorization(self):
        """Returns Spotipy Client."""
        token = util.prompt_for_user_token(
            username=self.configs['user'],
            scope=self.configs['scope'],
            client_id=self.configs['CLIENT_ID'],
            client_secret=self.configs['CLIENT_KEY'],
            redirect_uri=self.configs['redirect_uri'],
            show_dialog=True
            )
        self.spotipy = spotipy.Spotify(auth=token)

    def get_playlist_df(self, playlistId):
        """Returns a df with all info from the playlist's music."""
        if playlistId == 'saved-tracks':
            tracks = self.spotipy.current_user_saved_tracks()
        else:
            tracks = self.spotipy.user_playlist(
                user=self.configs['user'],
                playlist_id=playlistId
            )['tracks']
        trackList = []
        while (True):
            for item in tracks['items']:
                if 'track' in item:
                    track = item['track']
                else:
                    track = item
                if track is not None:
                    features = self.spotipy.audio_features([track['id']])
                    trackInfo = [
                        track['id'],
                        track['name'],
                        track['artists'][0]['name'],
                        track['popularity'],
                        features[0]['key'],
                        features[0]['energy'],
                        features[0]['speechiness'],
                        features[0]['acousticness'],
                        features[0]['instrumentalness'],
                        features[0]['valence'],
                        features[0]['tempo']
                    ]
                    trackList.append(trackInfo)
            if tracks['next']:
                tracks = self.spotipy.next(tracks)
            else:
                break
        return pd.DataFrame(data=trackList, columns=self.columns)

    def add_tracks_in_playlist(self, tracks, playlist_id):
        """Add a list of tracks id in a given playlist."""
        if len(tracks) > self.batch_limit:
            for i in range(0, len(tracks), self.batch_limit):
                self.spotipy.user_playlist_add_tracks(
                    user=self.configs['user'],
                    playlist_id=playlist_id,
                    tracks=tracks[(i):(self.batch_limit + i)]
                )
        else:
            self.spotipy.user_playlist_add_tracks(
                user=self.configs['user'],
                playlist_id=playlist_id,
                tracks=tracks
            )
        print('{} tracks have been added into the playlist {}'
              .format(len(tracks), playlist_id))
