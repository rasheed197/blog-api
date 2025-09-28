from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from src.utils.slug import generate_slug

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    
    # Relationship (1 user → many posts)
    # user.posts -> returns all current user posts
    posts = db.relationship("Post", back_populates="author", cascade="all, delete")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.username = self.email.split("@")[0]

    def __repr__(self):
        return f"<User with username {self.username}>"


class Post(db.Model):
    # core attributes
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    slug = db.Column(db.String(60), unique=True)
    content = db.Column(db.Text(), nullable=False)
    plublished_at = db.Column(db.DateTime, default=datetime.now())

    # categorizations
    category = db.Column(db.String(20))
    tag = db.Column(db.String(20))

    # Foreign Key
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    
    # Relationship back to user. post.author -> returns user
    author = db.relationship("User", back_populates="posts")

    # metadata attributes
    status = db.Column(db.String(10), default="draft")
    featured_image = db.Column(db.String(60))

    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.slug = generate_slug(self.title) + datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    def __repr__(self):
        return f"<Blog by author {self.slug}>"


# class Category(db.Model):
#     id = db.Column(db.Integer, primary_key=True)