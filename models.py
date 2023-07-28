# from poing import db
# from sqlalchemy import ForeignKey, DateTime, Column, Integer, String, DATE, Text, func, Boolean, Float, Table


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.String(80), unique=True, nullable=False)
#     videos = db.relationship('Video', backref='user', lazy=True)
#     keywords = db.relationship('Keyword', backref='user', lazy=True)

#     def __repr__(self):
#         return f'<User {self.username}>'

# class Video(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     video_id = db.Column(db.String(80), nullable=False)
#     time = db.Column(db.String(80), nullable=False)

# class Keyword(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     keyword = db.Column(db.String(80), nullable=False)
#     time = db.Column(db.String(80), nullable=False)