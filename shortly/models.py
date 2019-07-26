from shortly import db
from datetime import datetime


class Url(db.Model):
    __tablename__ = "url"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    destination = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, name, destination):
        import re

        self.name = re.sub('[^0-9a-zA-Zㄱ-힗-]', '', name)
        self.destination = destination \
            if 'http://' in destination or 'https://' in destination \
            else 'http://' + destination

    def __repr__(self):
        return '<Url %r>' % self.name
