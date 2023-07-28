from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = Api(app)



class test(Resource):
    def get(self):
        return {
	    "YouTubeBigBoxs": [{
			"image": "https: //i.ytimg.com/vi/3yluDg_GnfE/hq720.jpg?sqp=-oaymwEcCNAFEJQDSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLB-NoAzWEK-9CdzznuxAmXv6r0Vdw",
			"lengthTime": "9: 33",
			"title": "아침을 시작하는 5분 명상 | 아침명상, 아침 스트레칭",
			"channelName": "에일린 mind yoga"
		},
		{
			"image": "https: //i.E/hq720.jpg?sqp=-oaymwEcCNAFEJQDSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLB-NoAzWEK-9CdzznuxAmXv6r0Vdw",
			"lengthTime": "9: 33",
			"title": "2아침을 시작하는 5분 명상 | 아침명상, 아침 스트레칭",
			"channelName": "에일린 mind yoga"
		},
		{
			"image": "https: //i.ytimg.com/vi/3yluDg_GnfE/hq720.jpg?sqp=-oaymwEcCNAFEJQDSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLB-NoAzWEK-9CdzznuxAmXv6r0Vdw",
			"lengthTime": "9: 33",
			"title": "3아침을 시작하는 5분 명상 | 아침명상, 아침 스트레칭",
			"channelName": "에일린 mind yoga"
		},
		{
			"image": "https: //i.ytimg.com/vi/3yluDg_GnfE/hq720.jpg?sqp=-oaymwEcCNAFEJQDSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLB-NoAzWEK-9CdzznuxAmXv6r0Vdw",
			"lengthTime": "9: 33",
			"title": "4아침을 시작하는 5분 명상 | 아침명상, 아침 스트레칭",
			"channelName": "에일린 mind yoga"
		}
	]

}
        
api.add_resource(test, '/test')

class detail(Resource):
    def get(self):
        return {
        "YouTubeDetailBoxResult" : {
        "lengthTime": "9:33",
        "image": "https://i.ytimg.com/vi/3yluDg_GnfE/hq720.jpg?sqp=-oaymwEcCNAFEJQDSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLB-NoAzWEK-9CdzznuxAmXv6r0Vdw",
        "title" :"10분안에 잠드는 꿀잠 수면명상 [숙면을 위한 수면 유도 음악]",
                "channelName" : "감귤 카톡 안됨",
                "url": "https://www.youtube.com/embed/A52uLJwcYuo",
                "description": "#최유리 #플레이리스트 #playlist\n🍀구독 ❤️좋아요 💬댓글은 큰 힘이 됩니다.\n⭐️이 영상의 저작권은 '최유리' 가수님에게 있습니다.\n⭐️이 영상은 수익을 창출하지 않습니다.\n⭐️최신 앨범 발매 순으로 정렬한 목록입니다.\n\n#최유리 #Choiyuri #싱어송라이터 #Singersongwriter #최유리 #Choiyuri #플레이리스트 #playlist #전곡",
                "commentList" : ["노래들이 참 이쁘고 보석같다…감사합니다 좋은노래들 ^^", "최정훈의 밤의공연에서 처음 보고 알게되었는데 저도 모르게 자꾸 최유리님 감성에 매료되어 찾아보게 되네요. 노래를 듣고 있으몀 마음이 울어요"]
        }
}

api.add_resource(detail, '/detail')

app.run(host='0.0.0.0', debug=False)

# app.run(debug=True)