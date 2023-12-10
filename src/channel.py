from googleapiclient.discovery import build
import json
import datetime

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.api_key = os.environ.get('YOUTUBE_API_KEY')
        self.channel_id = channel_id
        self.title = None
        self.description = None
        self.url = None
        self.subscriber_count = None
        self.video_count = None
        self.view_count = None

        service = Channel.get_service()
        response = service.channels().list(part='snippet,statistics', id=channel_id).execute()

        if response['items']:
            channel_data = response['items'][0]
            snippet = channel_data['snippet']
            statistics = channel_data['statistics']

            self.title = snippet['title']
            self.description = snippet['description']
            self.url = f"https://www.youtube.com/channel/{channel_id}"
            self.subscriber_count = statistics['subscriberCount']
            self.video_count = statistics['videoCount']
            self.view_count = statistics['viewCount']

    def __str__(self):
        return f"self.name (self.link)"

    def __add__(self, other):
        if self.subscriber_count > other.subscriber_count:
            return str(self)
        else:
            return str(other)

    def __sub__(self, other):
        return self.subscriber_count - other.subscriber_count

    def __eq__(self, other):
        return self.subscriber_count == other.subscriber_count


    @classmethod
    def get_service(cls):
        with open('api_key.json') as f:
            api_key = json.load(f)['api_key']
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, filename):
        data = {
            "channel_id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }
        with open(filename, 'w') as f:
            json.dump(data, f)

    def print_info(self, dict_to_print: dict) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

    class Video:
        def __init__(self, video_id, title, link, views, likes):
            self.video_id = video_id
            self.title = title
            self.link = link
            self.views = views
            self.likes = likes

        def __str__(self):
            return self.title

    class PLVideo(Video):
        def __init__(self, video_id, title, link, views, likes, playlist_id):
            super().__init__(video_id, title, link, views, likes)
            self.playlist_id = playlist_id

    class PlayList:
        def init(self, _id, title=None, url=None):
            self.id = _id
            self.title = title
            self.url = url
            self.videos = []

        @property
        def total_duration(self):
            total_seconds = 0
            for video in self.videos:
                total_seconds += video.duration.total_seconds()
            return datetime.timedelta(seconds=total_seconds)

        def show_best_video(self):
            best_video = max(self.videos, key=lambda x: x.likes)
            return best_video.url

    class Video:
        def init(self, title, url, duration, likes):
            self.title = title
            self.url = url
            self.duration = duration
            self.likes = likes

    pl = PlayList('PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw')
    pl.title = "Moscow Python Meetup №81"
    pl.url = "https://www.youtube.com/playlist?list=PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw"
    video1 = Video("Video 1", "https://youtu.be/abc123", datetime.timedelta(minutes=30), 1000)
    video2 = Video("Video 2", "https://youtu.be/cUGyMzWQcGM", datetime.timedelta(minutes=45), 2000)
    video3 = Video("Video 3", "https://youtu.be/xyz456", datetime.timedelta(minutes=34), 1500)
    pl.videos.extend([video1, video2, video3])

    duration = pl.total_duration
    print(str(duration))  # Output: 1:49:00

    print(pl.show_best_video())  # Output: https://youtu.be/cUGyMzWQcGM

