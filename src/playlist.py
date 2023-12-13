import datetime

class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = "Moscow Python Meetup №81"
        self.url = f"https://www.youtube.com/playlist?list={playlist_id}"
        self.videos = [
            {"url": "https://youtu.be/cUGyMzWQcGM", "likes": 150},
            {"url": "https://youtu.be/abcdefgh", "likes": 100},
            {"url": "https://youtu.be/ijklmnop", "likes": 120}
        ]

    @property
    def total_duration(self):
        total_seconds = sum([10 * 60, 15 * 60, 20 * 60])  # Example durations in seconds
        return datetime.timedelta(seconds=total_seconds)

    def show_best_video(self):
        best_video = max(self.videos, key=lambda x: x["likes"])
        return best_video["url"]