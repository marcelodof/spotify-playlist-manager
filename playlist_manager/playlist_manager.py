"""Playlist Manager Class."""
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
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
        self.features = [
            "popularity",
            "key",
            "energy",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "valence",
            "tempo"
        ]

    def build_dataframe(self):
        """Return dataframe to be classified and model dataframe."""
        print('Building dataframe...')
        saved_tracks_df = self.spotipy.get_playlist_df('saved-tracks')
        sad_playlist_df = self.spotipy.get_playlist_df(sad_playlist_id)
        happy_playlist_df = self.spotipy.get_playlist_df(happy_playlist_id)

        # Building Unclassified Dataframe
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

    def run_classification(self):
        """Return dataframe with classification."""
        print('Running Classification...')
        # Splitting Dataset
        df_features = self.model_df[self.features]
        df_labels = self.model_df['label']
        df_features_train, df_features_test, df_labels_train, df_labels_test \
            = train_test_split(
                df_features,
                df_labels,
                test_size=0.2,
                random_state=0
            )

        # Training Model
        lg = LogisticRegression()
        lg.fit(df_features_train, df_labels_train)
        prediction = lg.predict(df_features_test)
        print(classification_report(df_labels_test, prediction))

        # Predicting
        labels = lg.predict(self.unclassified_df[self.features])
        self.df_results = self.unclassified_df.copy()
        self.df_results['label'] = labels

    def upload_classified_tracks(self):
        """Uploads classified tracks."""
        print('Uploading classified tracks...')
        tracks = {
            'happy_playlist_tracks':
                self.df_results['id'].loc[self.df_results['label'] == 1]
                .tolist(),
            'sad_playlist_tracks':
                self.df_results['id'].loc[self.df_results['label'] == 0]
                .tolist(),
        }
        self.spotipy.add_tracks_in_playlist(
            tracks=tracks['happy_playlist_tracks'],
            playlist_id=happy_playlist_id,
        )
        self.spotipy.add_tracks_in_playlist(
            tracks=tracks['sad_playlist_tracks'],
            playlist_id=sad_playlist_id,
        )
