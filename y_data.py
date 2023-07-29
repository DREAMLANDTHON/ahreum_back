from googleapiclient.discovery import build
from isodate import parse_duration
from googleapiclient.errors import HttpError
from config import YOUTUBE_API_KEY
from isodate import parse_duration




youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

class y_data:
    keyward = ''
    search_data = None
    def __init__(self, keyward = ''):#class생성시 키워드 입력, 키워드를 통해 검색 데이터 리스트 생성
        if keyward != '':
            self.keyward = keyward
            request = youtube.search().list(
                part="snippet",
                maxResults=10,
                q=self.keyward,
                type="video"
            )
            self.search_data = request.execute()
    def get_video_detail(self, video_id):
        title, des, thum = self.get_video_info(video_id)
        video_dict = {
            "YouTubeDetailBoxModel" : {
                "lengthTime" : self.get_video_duration(video_id),
                "image" : thum,
                "title" : title,
                "channelName" : self.get_channelName(video_id),
                "url" : self.get_video_url(video_id),
                "description" : des,
                "movieID" : video_id,
                "commentList" : self.get_comment_list(video_id)
            }
        }
        return video_dict
    def get_video_info(self, video_id):
        try:
            request = youtube.videos().list(
                part="snippet",
                id=video_id
            )
            response = request.execute()
            title = response['items'][0]['snippet']['title']
            description = response['items'][0]['snippet']['description']
            thumbnail = response['items'][0]['snippet']['thumbnails']['default']['url']
            return title, description, thumbnail
        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
            return None
    def get_video_data(self):#비디오 데이터 리스트 생성 - 구조 [{}] 리스트 안에 딕션너리
        video_list = []
        for item in self.search_data['items']:
            video_id = self.get_video_id(item)
            video_dict = {
            "YouTubeBigBoxs" : [{
                "image" : item['snippet']['thumbnails']['default']['url'],
                "lengthTiem" : self.get_video_duration(video_id),
                "title" : item['snippet']['title'],
                "channelName" : self.get_channelName(video_id),
                "movieID" : video_id
                
                }]
            }
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
        re=response['items'][0]['contentDetails']['duration']
        duration = parse_duration(re) # PT13S를 timedelta 객체로 변환
        seconds = int(duration.total_seconds()) # timedelta 객체를 초단위로 변환
        if hours // 3600 == 0:
            minutes = (seconds % 3600) // 60  # 남은 시간을 분으로 변환
            seconds = seconds % 60  # 남은 시간을 초로 변환
            formatted_duration = "{:02d}:{:02d}".format(minutes, seconds)
        else:
            hours = seconds // 3600  # 전체 시간(초)을 시간으로 변환
            minutes = (seconds % 3600) // 60  # 남은 시간을 분으로 변환
            seconds = seconds % 60  # 남은 시간을 초로 변환
            formatted_duration = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
        return formatted_duration
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