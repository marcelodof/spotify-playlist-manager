"""Spotipy Class."""
import spotipy
import spotipy.util as util


class Spotipy():
    """Spotipy Class Main Entry Point."""
    def __init__(self, configs):
        """Spotipy Init."""
        self.configs = configs
        self.get_authorization()

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
        self.spotify = spotipy.Spotify(auth=token)

    def get_playlist_df(self, id):
        """Returns all music info from a playlist."""
