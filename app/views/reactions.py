from app import app, USERS, POSTS
from flask import request, Response
from http import HTTPStatus


@app.post("/posts/<int:post_id>/reaction")
def add_reaction_on_the_post(post_id):
    data = request.get_json()
    reaction = data["reaction"]

    post = POSTS[post_id]
    post_owner_id = post.author_id
    post.reactions.append(reaction)
    USERS[post_owner_id].total_reactions += 1
    if post_id < 0 or post_id >= len(POSTS):
        return Response(status=HTTPStatus.BAD_REQUEST)

    return Response(status=HTTPStatus.CREATED)
