"""Playlist Manager."""
from playlist_manager.playlist_manager import PlaylistManager
from configs.configs import get_configs
import time


def main():
    """Playlist Manager Main Entry Point."""
    start_time = time.strftime('%X', time.gmtime(time.time()))
    print('Start time: ' + start_time)

    configs = get_configs()
    pm = PlaylistManager(configs)

    pm.build_dataframe()
    pm.run_classification()
    pm.upload_classified_tracks()

    end_time = time.strftime('%X', time.gmtime(time.time()))
    print('\n' + 'Start time: ' + start_time +
          '\n' + 'End time: ' + end_time)


if __name__ == '__main__':
    main()
