from app import app, USERS, models
from flask import request, Response
import json
from http import HTTPStatus
import re



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



@app.get("/users/leaderboard")
def get_sorted_users():
    data = request.get_json()
    sort_type = data["sort"]
    sorted_list = USERS

    if sort_type == "asc":
        for i in range(len(sorted_list) - 1):
            for j in range(len(sorted_list) - i - 1):
                if sorted_list[j].total_reactions > sorted_list[j + 1].total_reactions:
                    sorted_list[j], sorted_list[j + 1] = sorted_list[j + 1], sorted_list[j]

    elif sort_type == "desc":
        for i in range(len(sorted_list) - 1):
            for j in range(len(sorted_list) - i - 1):
                if sorted_list[j].total_reactions < sorted_list[j + 1].total_reactions:
                    sorted_list[j], sorted_list[j + 1] = sorted_list[j + 1], sorted_list[j]
    else:
        return Response(status=HTTPStatus.BAD_REQUEST)

    u = []
    for i in range(len(sorted_list)):
        q = dict()
        q["id"] = sorted_list[i].id
        q["first_name"] = sorted_list[i].first_name
        q["last_name"] = sorted_list[i].last_name
        q["email"] = sorted_list[i].email
        q["total_reactions"] = sorted_list[i].total_reactions
        u.append(q)
    new_dict = dict()
    new_dict["users"] = u

    response = Response(
        json.dumps(new_dict),
        HTTPStatus.CREATED,
        mimetype="application/json"
    )
    return response
