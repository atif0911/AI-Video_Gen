from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class VideoProject(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    topic = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default = "pending")

    script_text = db.Column(db.Text, nullable=True)
    audio_path = db.Column(db.String(200), nullable=True)
    video_path = db.Column(db.String(200), nullable=True)
    youtube_link = db.Column(db.String(200), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<VideoProject {self.topic}| Status: {self.status}>'