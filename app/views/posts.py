from app import app, USERS, POSTS, models
from flask import request, Response
import json
from http import HTTPStatus



@app.post("/posts/create")
def add_post():
    data = request.get_json()
    posts_id = len(POSTS)
    author_id = data["author_id"]
    text = data["text"]
    user = USERS[author_id]
    post = models.Post(posts_id, author_id, text)

    POSTS.append(post)
    user.add(posts_id)
    response = Response(
        json.dumps({
            "id": post.id,
            "author_id": post.author_id,
            "text": post.text,
            "reactions": post.reactions,
        }),
        HTTPStatus.CREATED,
        mimetype="application/json",
    )
    return response


@app.get("/posts/<int:post_id>")
def get_info_post(post_id):
    post = POSTS[post_id]
    if not (isinstance(post_id, int)) or post_id < 0 or post_id >= len(POSTS):
        return Response(status=HTTPStatus.BAD_REQUEST)

    response = Response(
        json.dumps({
            "id": post.id,
            "author_id": post.author_id,
            "text": post.text,
            "reactions": post.reactions,
        }),
        HTTPStatus.CREATED,
        mimetype="application/json",
    )
    return response


@app.get("/users/<int:user_id>/posts")
def get_all_posts(user_id):
    sort_type = request.get_json()["sort"]
    all_posts = USERS[user_id].posts  # список id-шников постов нашего пользователя
    s = []  # список постов (объектов)
    for number in all_posts:
        s.append(POSTS[number])

    if sort_type == "asc":
        for i in range(len(s) - 1):
            for j in range(len(s) - i - 1):
                if len(s[j].reactions) > len(s[j + 1].reactions):
                    s[j], s[j + 1] = s[j + 1], s[j]

    elif sort_type == "desc":
        for i in range(len(s) - 1):
            for j in range(len(s) - i - 1):
                if len(s[j].reactions) < len(s[j + 1].reactions):
                    s[j], s[j + 1] = s[j + 1], s[j]

    else:
        return Response(status=HTTPStatus.BAD_REQUEST)
    u = []
    for i in range(len(s)):
        q = dict()
        q["id"] = s[i].id
        q["author_id"] = s[i].author_id
        q["text"] = s[i].text
        q["reactions"] = s[i].reactions
        u.append(q)
    new_dict = dict()
    new_dict["posts"] = u

    response = Response(
        json.dumps(new_dict),
        HTTPStatus.CREATED,
        mimetype="application/json"
    )
    return response
