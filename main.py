"""Playlist Manager."""
from playlist_manager.playlist_manager import PlaylistManager
from configs.configs import get_configs


def main():
    """Playlist Manager Main Entry Point."""
    configs = get_configs()
    pm = PlaylistManager(configs)
    pm.build_dataframe()


if __name__ == '__main__':
    main()
