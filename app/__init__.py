from flask import Flask

app = Flask(__name__)
USERS = []  # list of users
POSTS = []  # user's posts

from app import views_all, models, views, tests
