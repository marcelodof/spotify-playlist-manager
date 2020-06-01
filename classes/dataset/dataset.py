"""Dataset Class."""
import pandas as pd
from services.spotipy.spotipy import Spotipy


class Dataset():
    """Dataset Class Main Entry Point."""
    def __init__(self, configs):
        """Init Dataset."""
        self.configs = configs
        self.df = pd.DataFrame()
        self.spotipy = Spotipy(configs)

    def get_dataset(self):
        return self.df
