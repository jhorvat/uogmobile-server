from functools import wraps
from flask import Blueprint, request, session, send_file, abort, jsonify
from flask import current_app as app

from .navigator import Navigator

mod = Blueprint('student_dir', __name__, url_prefix="/studentdir")

@mod.route("/lookup/<central_id>", methods=['GET'])
def lookup(central_id):
    email = "{0}@mail.uoguelph.ca"

    with Navigator() as wd:
        name = wd.lookup_student(email.format(central_id))

    if not name:
        abort(404)

    return jsonify({
        "name": name,
        "central_id": central_id
    })
