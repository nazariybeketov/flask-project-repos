from flask import Flask

app = Flask(__name__)
USERS = [] # list of users


from app import views, models