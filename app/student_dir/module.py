from functools import wraps
from flask import Blueprint, request, session, send_file, abort, jsonify
from flask import current_app as app

from . import constants
from .navigator import Navigator

mod = Blueprint('student_dir', __name__, url_prefix="/studentdir")

@mod.route("/lookup", methods=['POST'])
def lookup():
    data = request.get_json()
    email = "{0}@mail.uoguelph.ca"

    if data and "central" in data and data["central"]:
        email = email.format(data["central"])
    else:
        abort(400)

    with Navigator() as wd:
        wd.lookup_student(email)
