from googleapiclient.discovery import build
from isodate import parse_duration
from googleapiclient.errors import HttpError
from config import YOUTUBE_API_KEY

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

class y_data:
    keyward = ''
    search_data = None
    def __init__(self, keyward):#class생성시 키워드 입력, 키워드를 통해 검색 데이터 리스트 생성
        self.keyward = keyward
        request = youtube.search().list(
            part="snippet",
            maxResults=10,
            q=self.keyward,
            type="video"
        )
        self.search_data = request.execute()
        
    def get_video_data(self):#비디오 데이터 리스트 생성 - 구조 [{}] 리스트 안에 딕션너리
        video_list = []
        for item in self.search_data['items']:
            video_id = self.get_video_id(item)
            video_dict = {}
            video_dict['video_id'] = video_id
            video_dict['title'] = item['snippet']['title']
            video_dict['description'] = item['snippet']['description']
            video_dict['channelName'] = self.get_channelName(video_id)
            video_dict['thumbnail'] = item['snippet']['thumbnails']['default']['url']
            video_dict['url'] = self.get_video_url(video_id)
            video_dict['duration'] = self.get_video_duration(video_id)
            video_dict['comment_list'] = self.get_comment_list(video_id)
            video_list.append(video_dict)
        return video_list
    def get_video_id(self, item):
        video_id = item["id"]["videoId"]
        return video_id
    def get_video_url(self, video_id):
        return f"https://www.youtube.com/embed/{video_id}"
    def get_video_duration(self, video_id):
        request = youtube.videos().list(
            part="contentDetails",
            id=video_id
        )
        response = request.execute()
        return response['items'][0]['contentDetails']['duration']
    def get_comment_list(self, video_id):
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=10,  # Change this value to get more comments
        )
        try:
            response = request.execute()
        except HttpError as e:
            print(f"Error: {e}")
            return []
        response = request.execute()
        comment_list = []
        for item in response['items']:
            comment_list.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
        return comment_list
    def get_channelName(self, video_id):
        request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
        response = request.execute()
        channel_id = response['items'][0]['snippet']['channelId']
        request = youtube.channels().list(
            part="snippet",
            id=channel_id
        )
        response = request.execute()
        return response['items'][0]['snippet']['title']

if __name__ == '__main__':
    test = y_data('김밥')
    data_list = test.get_video_data()
    print(data_list)
    print()
    print()
    for data in data_list:
        print(f"title : {data['title']}")
        print(f"description : {data['description']}")
        print(f"duration : {data['duration']}")
        print(f"thumbnail : {data['thumbnail']}")
        print(f"url : {data['url']}")