import datetime
from app import db
from sqlalchemy.dialects.postgresql import JSON

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), unique=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, question):
        self.question = question

    def __repr__(self):
        return '<id {}>'.format(self.id)