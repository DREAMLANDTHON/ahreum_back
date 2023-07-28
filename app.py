from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import p_keyword
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import recommand
current_file_path = os.path.abspath(__file__)
# 이 파일의 디렉토리 경로
current_directory = os.path.dirname(current_file_path)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(current_directory, 'test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # SQLAlchemy 이벤트를 추적하지 않도록 설정
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(80), unique=True, nullable=False)
    videos = db.relationship('Video', backref='user', lazy=True)
    keywords = db.relationship('Keyword', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    video_id = db.Column(db.String(80), nullable=False)
    time = db.Column(db.String(80), nullable=False)

class Keyword(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    keyword = db.Column(db.String(80), nullable=False)
    time = db.Column(db.String(80), nullable=False)

class videoList(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str)
        parser.add_argument('keyward', type=str)  # user_id를 받아오도록 추가
        args = parser.parse_args()
        user = User.query.filter_by(user_id=args['user_id']).first()

        if user is None:
            return {'error': 'User not found'}, 400
        re = recommand.check_rate(args['keyward'])        
        return re

class keyword_api(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('video_id', type=str)
        parser.add_argument('user_id', type=str)  # user_id를 받아오도록 추가
        args = parser.parse_args()
        re = p_keyword.get_key_wards(args['video_id'])
        
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 받아온 user_id를 가진 유저를 찾습니다.
        user = User.query.filter_by(user_id=args['user_id']).first()

        # 유저가 없을 경우 새 유저를 생성합니다.
        if user is None:
            return {'error': 'User not found'}, 400

        # Video 인스턴스를 생성하고 DB에 추가합니다.
        video = Video(user_id=user.id, video_id=args['video_id'], time = time)
        db.session.add(video)
        for value in re.values :
            key_data = Keyword(user_id=user.id, keyword = value, time = time)
            db.session.add(key_data)
        db.session.commit()
        return re
    
class UserApi(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str)
        args = parser.parse_args()

        user = User(user_id=args['user_id'])
        db.session.add(user)
        db.session.commit()

        return {'message': 'User successfully created.'}, 201

class UsersApi(Resource):
    def get(self):
        users = User.query.all()
        return [{'id': user.id, 'user_id': user.user_id} for user in users]

class VideosApi(Resource):
    def get(self):
        videos = Video.query.all()
        return [{'id': video.id, 'user_id': video.user_id, 'video_id': video.video_id, 'time': video.time} for video in videos]

class KeywordsApi(Resource):
    def get(self):
        keywords = Keyword.query.all()
        return [{'id': keyword.id, 'user_id': keyword.user_id, 'keyword': keyword.keyword, 'time': keyword.time} for keyword in keywords]

api.add_resource(UsersApi, "/users")
api.add_resource(VideosApi, "/videos")
api.add_resource(KeywordsApi, "/keywords")


api.add_resource(keyword_api, "/keyword-api")
api.add_resource(UserApi, "/user-api")

api.add_resource(videoList, "/videoList")
if __name__ == '__main__':
    with app.app_context():  # Add this line
        db.create_all()  # This should now work
    app.run(host='0.0.0.0', debug=True)
