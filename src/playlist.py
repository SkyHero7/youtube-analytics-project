import os
import datetime
import requests
from googleapiclient.discovery import build

from src.video import Video

class PlayList:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)
    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id
        self.title = ""
        self.url = ""
        self.videos = [Video(video_id) for video_id in self.video_ids]

        self.get_playlist_info()

    def get_playlist_info(self):
        api_url = os.getenv('YT_API_KEY')
        response = requests.get(api_url)
        data = response.json()

        self.title = data["title"]
        self.url = data["url"]
        self.videos = data["videos"]

    @property
    def total_duration(self):
        total_seconds = sum([video["duration"] for video in self.videos])
        return datetime.timedelta(seconds=total_seconds)

    def show_best_video(self):
        best_video = max(self.videos, key=lambda x: x["likes"])
        return best_video["url"]