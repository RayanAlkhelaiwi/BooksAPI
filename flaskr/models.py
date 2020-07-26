import os
from sqlalchemy import Column, String, Integer, Boolean, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_name = 'books'
database_path = 'postgres://{}@localhost:5432/{}'.format(
    'rayanalkhelaiwi', database_name)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Book(db.Model):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    author = Column(String)
    title = Column(String)
    rating = Column(Integer)

    def __init__(self, author, title, rating):
        self.author = author
        self.title = title
        self.rating = rating

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'author': self.author,
            'title': self.title,
            'rating': self.rating,
        }
