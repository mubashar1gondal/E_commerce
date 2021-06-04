from datetime import datetime as dt
from app import db
from flask_login import UserMixin
from app import login_manager
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import Post

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def followed_posts(self):
        followed = Post.query.join(
            followers,
            (followers.c.followed_id == Post.user_id)
        ).filter(followers.c.follower_id == self.id)
        self_posts = Post.query.filter_by(user_id=self.id)
        all_posts = followed.union(self_posts).order_by(Post.created_on.desc())
        return all_posts

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            db.session.commit()

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            db.session.commit()

    def set_email(self):
      self.email = f"{self.first_name}{self.last_name[0]}@codingtemple.com".lower()


    def from_dict(self, data):
        for attr in ['first_name', 'last_name', 'email', 'password']:
            if attr in data:
                if attr == 'email':
                    setattr(self, attr, data[attr].lower())
                else:
                    setattr(self, attr, data[attr])

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'created_on': dt.strftime(self.created_on, '%m/%d/%Y')
        }

    def save(self):
        self.set_password(self.password)
        db.session.add(self)
        db.session.commit()  

    def set_password(self, pword):
        self.password = generate_password_hash(pword)

    def check_password(self, pword):
        return check_password_hash(self.password, pword)

    def __repr__(self):
        return f'<User: {self.email}>'

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)
