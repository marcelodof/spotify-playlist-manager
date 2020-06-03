"""Playlist Manager Class."""
from services.spotipy.spotipy import Spotipy
import pandas as pd

sad_playlist_id = '66StSH0fC8xwrAy6jStQSD'
happy_playlist_id = '7bq3dy7YjKcTDvd4DrLMzN'


class PlaylistManager():
    """PlaylistManager Main Entry Point."""
    def __init__(self, configs):
        """PlaylistManager Init."""
        self.configs = configs
        self.spotipy = Spotipy(configs)

    def build_dataframe(self):
        """Return dataframe to be classified."""
        print('Building dataframe...')
        print('Getting Saved Tracks Dataframe...')
        saved_tracks_df = self.spotipy.get_playlist_df('saved-tracks')
        print('Getting Sad Playlist Dataframe...')
        sad_playlist_df = self.spotipy.get_playlist_df(sad_playlist_id)
        print('Getting Happy Playlist Dataframe...')

        # Building Unclassified Dataframe
        happy_playlist_df = self.spotipy.get_playlist_df(happy_playlist_id)
        saved_tracks_set_id = set(saved_tracks_df['id'])
        sad_playlist_set_id = set(sad_playlist_df['id'])
        happy_playlist_set_id = set(happy_playlist_df['id'])
        classified_set_id = happy_playlist_set_id.union(sad_playlist_set_id)
        unclassified_set_id = saved_tracks_set_id.difference(classified_set_id)
        self.unclassified_df = saved_tracks_df\
            .loc[saved_tracks_df['id'].isin(unclassified_set_id)]

        # Building Model Dataframe
        sad_playlist_df['label'] = 0
        happy_playlist_df['label'] = 1
        self.model_df = pd.concat(
            [sad_playlist_df, happy_playlist_df],
            ignore_index=True
        )

        print(self.unclassified_df.head())
        print(self.model_df.head())
