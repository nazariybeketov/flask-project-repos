from app import app, USERS


@app.route("/")
def index():
    return f'<h1>{USERS}</h1>'

