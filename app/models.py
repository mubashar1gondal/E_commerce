from datetime import datetime as dt
from app import db
from flask_login import UserMixin
from app import login_manager
from werkzeug.security import check_password_hash, generate_password_hash

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    user_id = db.Column(db.ForeignKey('user.id'))

    # def from_dict(self):
    #     pass

    def to_dict(self):
        from app.blueprints.authentication.models import User

        return {
            'id': self.id,
            'body': self.body,
            'user': User.query.get(self.user_id).to_dict(),
            'created_on': {
                'real': self.created_on,
                'pretty': dt.strftime(self.created_on, '%m/%d/%Y')
            }
        }

    def __repr__(self):
        return f'<Post: [{self.user.email}]: {self.body[:20]}...>'