import os
import datetime
from googleapiclient.discovery import build

from src.video import Video

class PlayList:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id: str) -> None:
        self.url: str | None = None
        self.title: str | None = None
        self.playlist_id: str = playlist_id
        self.get_playlist_info()

    def get_playlist_info(self) -> None:
        """Получаем данные по API и инициализируем ими экземпляр класса."""
        playlist_info = self.youtube.playlists().list(id=self.playlist_id, part='snippet', ).execute()
        self.title = playlist_info['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    def get_playlist_videos(self) -> dict:
        """Возвращает ответ API на запрос всех видео плейлиста."""
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()

        # получить все id видеороликов из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        # получит данные по каждому видео
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()
        return video_response

    @property
    def total_duration(self) -> datetime.timedelta:
        """Возвращает суммарную длительность плей-листа в формате 'datetime.timedelta' (hh:mm:ss))."""
        video_response = self.get_playlist_videos()

        duration = datetime.timedelta()
        for video in video_response['items']:
            # Длительности YouTube-видео представлены в ISO 8601 формате
            iso_8601_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_8601_duration)

        return duration

    def show_best_video(self) -> str:
        """Выводит ссылку на самое залайканое видео в плейлисте."""
        video_response = self.get_playlist_videos()

        best_video = max([video for video in video_response['items']], key=lambda x: x['statistics']['likeCount'])
        return f"https://youtu.be/{best_video['id']}"