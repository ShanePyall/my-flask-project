from flask import Flask, request, render_template
import json

app = Flask(__name__)


@app.route('/add', methods=['GET', 'POST'])
def add():
    # Will create a new post, with the data filled in from html and store in json file
    if request.method == 'POST':
        with open("data-structure.json", "r") as readable:
            post_list = json.load(readable)

        next_id = int(post_list[-1]['id']) + 1
        author = request.form.get('author', "Author")
        title = request.form.get('title', "Title")
        content = request.form.get("content", "Content")

        post_dict = {'id': next_id,
                     "author": author,
                     "title": title,
                     "content": content}

        post_list.append(post_dict)
        with open("data-structure.json", "w") as writable:
            writable.write(json.dumps(post_list))
        return index()
    return render_template('add.html')


@app.route('/delete/<post_id>')
def delete(post_id):
    # Receives post ID as path from html, deletes post in json file with id.
    with open("data-structure.json", "r") as readable:
        post_list = json.load(readable)
        for item in post_list:
            if item['id'] == int(post_id):
                post_list.remove(item)
    with open("data-structure.json", "w") as writable:
        writable.write(json.dumps(post_list))
    return index()


@app.route('/update/<post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Checks if id is valid, then replaces any data that was altered. if none, keep old data.
    found_post = None
    with open("data-structure.json", "r") as readable:
        post_list = json.load(readable)
        for post in post_list:
            if post["id"] == int(post_id):
                found_post = post
    if found_post is None:
        return "Post not found", 404

    if request.method == 'POST':
        found_post["author"] = request.form.get('author')
        found_post["title"] = request.form.get('title')
        found_post["content"] = request.form.get('content')

        for item in post_list:
            if item['id'] == int(post_id):
                item = found_post
        with open("data-structure.json", "w") as writable:
            writable.write(json.dumps(post_list))
        return index()

    return render_template('update.html', post=found_post)


@app.route('/')
def index():
    # Sends a list of blog posts to a template for display
    with open("data-structure.json", "r") as readable:
        posts = json.load(readable)
    return render_template('index.html', posts=posts)  # renders file with value posts replaced with a list.


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
