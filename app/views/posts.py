from app import app, USERS, POSTS, models
from flask import request, Response
import json
from http import HTTPStatus


@app.post("/posts/create")
def add_new_post():
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
def get_post_info(post_id):
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
def get_sorted_posts_of_our_user(user_id):
    sort_type = request.get_json()["sort"]
    all_posts = USERS[user_id].posts  # список id-шников постов нашего пользователя
    lst_pst_obj = []  # список постов (объектов)
    for number in all_posts:
        lst_pst_obj.append(POSTS[number])

    if sort_type == "asc":
        for i in range(len(lst_pst_obj) - 1):
            for j in range(len(lst_pst_obj) - i - 1):
                if len(lst_pst_obj[j].reactions) > len(lst_pst_obj[j + 1].reactions):
                    lst_pst_obj[j], lst_pst_obj[j + 1] = lst_pst_obj[j + 1], lst_pst_obj[j]

    elif sort_type == "desc":
        for i in range(len(lst_pst_obj) - 1):
            for j in range(len(lst_pst_obj) - i - 1):
                if len(lst_pst_obj[j].reactions) < len(lst_pst_obj[j + 1].reactions):
                    lst_pst_obj[j], lst_pst_obj[j + 1] = lst_pst_obj[j + 1], lst_pst_obj[j]

    else:
        return Response(status=HTTPStatus.BAD_REQUEST)
    temp_lst_pst = []
    for i in range(len(lst_pst_obj)):
        temp_dct_pst = dict()
        temp_dct_pst["id"] = lst_pst_obj[i].id
        temp_dct_pst["author_id"] = lst_pst_obj[i].author_id
        temp_dct_pst["text"] = lst_pst_obj[i].text
        temp_dct_pst["reactions"] = lst_pst_obj[i].reactions
        temp_lst_pst.append(temp_dct_pst)
    new_dict = dict()
    new_dict["posts"] = temp_lst_pst

    response = Response(
        json.dumps(new_dict),
        HTTPStatus.CREATED,
        mimetype="application/json"
    )
    return response
