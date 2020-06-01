"""Playlist Manager."""
from classes.dataset.dataset import Dataset
from configs.configs import get_configs


def main():
    """Playlist Manager Main Entry Point."""
    configs = get_configs()
    print(configs)
    dataset = Dataset(configs)


if __name__ == '__main__':
    main()
