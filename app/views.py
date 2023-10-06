from app import app, USERS, models
from flask import request, Response
import json
from http import HTTPStatus
import re

@app.route("/")
def index():
    return "<h1>Hello World</h1>"


@app.post("/users/create")
def user_create():
    users_id = len(USERS)
    data = request.get_json()
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return Response(status=HTTPStatus.BAD_REQUEST)


    user = models.User(users_id, first_name, last_name, email)
    USERS.append(user)
    response = Response(
        json.dumps({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "total_reactions": user.total_reactions,
            "posts": user.posts,
        }),
        HTTPStatus.CREATED,
        mimetype="application/json",
    )
    return response


@app.get("/users/<int:user_id>")
def get_user(user_id):
    if not (isinstance(user_id, int)) or user_id < 0 or user_id >= len(USERS):
        return Response(status=HTTPStatus.NOT_FOUND)

    user = USERS[user_id]
    response = Response(
        json.dumps({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "total_reactions": user.total_reactions,
            "posts": user.posts,
        }),
        HTTPStatus.CREATED,
        mimetype="application/json",
    )
    return response


