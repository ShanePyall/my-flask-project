import flask
from flask import render_template
import json

app = flask(__name__)


@app.route('/')
def index():
    # Sends a list of blog posts to a template for display
    with open("data-structures.json", "r") as readable:
        blog_posts = json.loads(readable.read())
    return render_template('index.html', posts=blog_posts) # renders file with value posts replaced with a list.


if __name__ == '__main__':
    app.run()
