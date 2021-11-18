import uuid

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class UserDB(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(48), nullable=True)
    username = db.Column(db.String(24), unique=True, nullable=False)
    pass_hash = db.Column(db.String(128), nullable=False)
    # hash value
    username_hash = db.Column(db.String(36), nullable=False)
    profile_img = db.Column(db.TEXT(1200), nullable=False)

class PostDB(db.Model):
    __tablename__ = 'posts'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    author = db.Column(db.String(24), db.ForeignKey('users.username'), nullable=False)
    num_likes = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    mimetype = db.Column(db.String(1000), nullable=True)

class LikeDB(db.Model):
    __tablename__ = 'likes'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(24), db.ForeignKey('users.username'), nullable=False)
    post_or_comment = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=True)
    like_type = db.Column(db.Boolean, nullable=False)

class TagDB(db.Model):
    __tablename__ = 'tags'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)

class PostTagDB(db.Model):
    __tablename__ = 'posts_tags'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

