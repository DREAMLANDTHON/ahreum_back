from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class test(Resource):
    def get(self):
        return {
                "image": '이미지에요',
                "lengthTime": '영상길이에요',
                "title": '제목이에요',
                "channelName" : '채널이름이에요'
                }
        
api.add_resource(test, '/test')