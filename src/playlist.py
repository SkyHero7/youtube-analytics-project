import datetime
import requests


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = ""
        self.url = ""
        self.videos = []

        self.get_playlist_info()

    def get_playlist_info(self):
        api_url = f"https://api.getplaylistinfo.com/{self.playlist_id}"
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