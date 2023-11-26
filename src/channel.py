import requests
from googleapiclient.discovery import build
import json

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.api_key = 'AIzaSyBZ76ebMl_GDynQb9wNWbIvrREj4J3mISQ'
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

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        url = f'https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={self.channel_id}&key={self.api_key}'
        response = requests.get(url)
        data = response.json()

        if 'items' in data:
            channel_info = data['items'][0]
            snippet = channel_info['snippet']
            statistics = channel_info['statistics']

            print({
                "title": snippet['title'],
                "description": snippet['description'],
                "subscriberCount": statistics['subscriberCount'],
                "viewCount": statistics['viewCount'],
                "videoCount": statistics['videoCount']
            })

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

