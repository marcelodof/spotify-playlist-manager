"""Spotipy Class."""
import spotipy
import spotipy.util as util
import pandas as pd


class Spotipy():
    """Spotipy Class Main Entry Point."""
    def __init__(self, configs):
        """Spotipy Init."""
        self.configs = configs
        self.get_authorization()
        self.columns = [
            "id",
            # "url",
            "name",
            # "artist",
            # "album",
            # "explicit",
            "popularity",
            # "duration_ms",
            "key",
            # "mode",
            # "time_signature",
            # "danceability",
            "energy",
            "speechiness",
            "acousticness",
            "instrumentalness",
            # "liveness",
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
                        # track['external_urls']['spotify'],
                        track['name'],
                        # track['artists'][0]['name'],
                        # track['album']['name'],
                        # track['explicit'],
                        track['popularity'],
                        # track['duration_ms'],
                        features[0]['key'],
                        # features[0]['mode'],
                        # features[0]['time_signature'],
                        # features[0]['danceability'],
                        features[0]['energy'],
                        features[0]['speechiness'],
                        features[0]['acousticness'],
                        features[0]['instrumentalness'],
                        # features[0]['liveness'],
                        features[0]['valence'],
                        features[0]['tempo']
                    ]
                    trackList.append(trackInfo)
            if tracks['next']:
                break
                tracks = self.spotipy.next(tracks)
            else:
                break
        return pd.DataFrame(data=trackList, columns=self.columns)
