from googleapiclient.discovery import build
import json
import os

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

    def print_info(dict_to_print: dict) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

