from app import app, USERS, models
from flask import request, Response, url_for
import json
from http import HTTPStatus
import re
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("agg")


@app.post("/users/create")
def user_create():
    users_id = len(USERS)
    data = request.get_json()
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email) or (
        email in [user.email for user in USERS]
    ):
        return Response("Ошибка при вводе почты", status=HTTPStatus.BAD_REQUEST)

    user = models.User(users_id, first_name, last_name, email)
    USERS.append(user)
    response = Response(
        json.dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "total_reactions": user.total_reactions,
                "posts": user.posts,
            }
        ),
        HTTPStatus.CREATED,
        mimetype="application/json",
    )
    return response


@app.get("/users/<int:user_id>")
def get_users_info(user_id):
    if not (isinstance(user_id, int)) or user_id < 0 or user_id >= len(USERS):
        return Response(status=HTTPStatus.NOT_FOUND)

    user = USERS[user_id]
    response = Response(
        json.dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "total_reactions": user.total_reactions,
                "posts": user.posts,
            }
        ),
        HTTPStatus.CREATED,
        mimetype="application/json",
    )
    return response


@app.get("/users/leaderboard")
def get_sorted_users():
    data = request.get_json()
    sorted_list = USERS
    type_1 = data["type"]
    if type_1 == "graph":
        for i in range(len(sorted_list) - 1):
            for j in range(len(sorted_list) - i - 1):
                if sorted_list[j].total_reactions > sorted_list[j + 1].total_reactions:
                    sorted_list[j], sorted_list[j + 1] = (
                        sorted_list[j + 1],
                        sorted_list[j],
                    )

        user_names = [f"{user.first_name} {user.last_name}" for user in sorted_list]
        user_reactions = [user.total_reactions for user in sorted_list]
        plt.bar(user_names, user_reactions)
        plt.xlabel("User names")
        plt.ylabel("Amount of user's reactions")
        plt.title("Leaderboard")
        plt.savefig("app/static/users_leaderboard.png")

        return Response(
            f"""<img src= "{url_for('static', filename='users_leaderboard.png')}">""",
            status=HTTPStatus.OK,
            mimetype="text/html",
        )

    sort_type = data["sort"]

    if sort_type == "asc" and type_1 == "list":
        for i in range(len(sorted_list) - 1):
            for j in range(len(sorted_list) - i - 1):
                if sorted_list[j].total_reactions > sorted_list[j + 1].total_reactions:
                    sorted_list[j], sorted_list[j + 1] = (
                        sorted_list[j + 1],
                        sorted_list[j],
                    )

    elif sort_type == "desc" and type_1 == "list":
        for i in range(len(sorted_list) - 1):
            for j in range(len(sorted_list) - i - 1):
                if sorted_list[j].total_reactions < sorted_list[j + 1].total_reactions:
                    sorted_list[j], sorted_list[j + 1] = (
                        sorted_list[j + 1],
                        sorted_list[j],
                    )
    else:
        return Response(status=HTTPStatus.BAD_REQUEST)

    temp_usrs_list = []
    for i in range(len(sorted_list)):
        temp_usrs_dct = dict()
        temp_usrs_dct["id"] = sorted_list[i].id
        temp_usrs_dct["first_name"] = sorted_list[i].first_name
        temp_usrs_dct["last_name"] = sorted_list[i].last_name
        temp_usrs_dct["email"] = sorted_list[i].email
        temp_usrs_dct["total_reactions"] = sorted_list[i].total_reactions
        temp_usrs_list.append(temp_usrs_dct)
    new_dict = dict()
    new_dict["users"] = temp_usrs_list

    response = Response(
        json.dumps(new_dict), HTTPStatus.CREATED, mimetype="application/json"
    )
    return response
