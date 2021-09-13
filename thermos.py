from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash


app = Flask(__name__)

bookmarks = []
app.config["SECRET_KEY"] = b'}C\xe7\xc5!\x7f\x94\xdb\xc8\xe3\xb5\xa7\x82l:^/\x10\x8a\x1f;\xe0\x96\xe5'


def store_bookmark(url):
    bookmarks.append(dict(
        url = url,
        user = "Bobberson",
        date = datetime.utcnow()
    ))

def new_bookmarks(num):
    return sorted(bookmarks, key=lambda bm: bm["date"], reverse=True)[:num]

class User:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def initials(self):
        return "{}. {}.".format(self.firstname[0], self.lastname[0])

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Title passed from view to template", user=User("Bob", "Bobberson"), new_bookmarks=new_bookmarks(5))

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        url = request.form["url"]
        store_bookmark(url)
        flash("Stored bookmark '{}'".format(url))
        return redirect(url_for("index"))
    return render_template("add.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500



if __name__ == '__main__':
    app.run(debug=True)
