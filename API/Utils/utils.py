from flask import Blueprint, render_template

utils = Blueprint("utils", __name__)

@utils.route("/")
def document():
    return render_template("index.html")