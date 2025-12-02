from flask import Blueprint

root_views = Blueprint(
    "root",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@root_views.route("/")
def index():
    return "Hello World!"
