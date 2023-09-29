"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    def __repr__(self):
        p = self
        return f" Hello my name is {p.first_name} {p.last_name}, here is my user picture {p.image_url}"
    
    # def get_first_name(cls, first_name):
    #  return cls.query.filter(first_name)
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                     nullable=False,
                     unique=True)
    last_name = db.Column(db.String(50),
                     nullable=False,
                     unique=True)
    image_url = db.Column(db.String, nullable=True)


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(50),
                     nullable=False,
                     unique=True)
    content = db.Column(db.String(500),
                     nullable=False,
                     unique=True)
    created_at = db.Column(db.DateTime)

    user_id = db.Column(db.ForeignKey('users.id'))

    user_post = db.relationship('User')

    post_tags = db.relationship('PostTag', backref = 'posts')


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    tag_name = db.Column(db.String, nullable= False, unique = True)

    post_tags = db.relationship('PostTag', backref = 'tags')

class PostTag(db.Model):
    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer,
                          db.ForeignKey("posts.id"),
                          nullable = False,
                          primary_key=True)
    
    tag_id = db.Column(db.Integer,
                          db.ForeignKey("tags.id"),
                          nullable = False,
                          primary_key=True)
