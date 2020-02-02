from datetime import datetime
from app import db



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    tasks = db.relationship('Task', backref='author', lazy='dynamic')
    def __repr__(self):
        return f'User {self.username}'


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    body = db.Column(db.String(140))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Task {self.body}'