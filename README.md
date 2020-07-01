# Spotify Playlist Manager

## Introduction

Before we start, a bit of context on what the problem is my and how I want to solve it. First of all, I am a very big music fan and I listen to a lot of different and strange stuff. Whenever I am in a more happy mood, I listen to one playlist, but when I fell more in a sad mood, I listen to another playlist. I have done this for about 3 years now. And to define which songs should go to each playlist, I had to listen and classify it by my standards. However, when I started learning a bit about Data Science, I realized that this could be automatizated. So I started working on it.

This program will build a dataset, of all the songs in 'Liked Songs', train the model, and then add the songs labeled to each playlist.

## Setup

First, it is necessary to install the following dependencies:
* pandas
* scikit-learn
* boto3
* spotipy

Then, so that we can access Spotify API, the client key and secret are required. They can be found in the [Spoitfy Developer website](https://developer.spotify.com/dashboard/applications).
Mine secrets were saved in AWS Secret Manager. There, you can add other secrets for your own application.
So, to get those keys, a new file with the AWS secrets must be added, called **credentials.py**. Which contains a function *get_credentials*, that returns a object:
```
{
    'AWS_SECRET_KEY_ID': '',
    'AWS_SECRET_ACCESS_KEY': ''
}
```

Last but not least, there is the playlists IDs, added as environment variables in the *playlist_manager.py* file. Those IDs are for my own playlists, just change to the playlists you want.

To better understand the **spotipy** setup, I recommend checking the library documentation [here](https://spotipy.readthedocs.io/en/2.13.0/).

## Running

In order to run the program, after all the configuration is made, just run the code:
` python3 main.py `
It will open a window in the browser, to log in to Spotify.
After doing that, the program should run without more interruptions.
In the end, it will print the classification report to showcase the model performance.