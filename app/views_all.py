from app import app, USERS


@app.route("/")
def index():
    return f"<h1>Hello</h1>"
