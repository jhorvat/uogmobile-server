import io
from functools import wraps
from flask import Blueprint, request, session, send_file, abort, jsonify
from flask import current_app as app
from datetime import datetime, timedelta

from . import constants
from .navigator import Navigator

# TODO: Migrate to WebDriver to context manager maybe
mod = Blueprint('web_advisor', __name__, url_prefix="/webadvisor")

def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """
        Get the WebAdvisor cookie payload
        """
        if "cookies" not in session:
            abort(403)

        return f(*args, **kwargs)
    return decorated_function

@mod.route("/login", methods=['POST'])
def login():
    data = request.get_json()

    if "cookie" in data and data["cookie"]:
        # Separate the cookies string into a list of key, value tuples
        data["cookie"] = [cookie.split("=", 1) for cookie in data["cookie"].replace(" ", "").split(";")]
    else:
        abort(400)

    cookie_payload = constants.WEB_ADVISOR_COOKIES_TEMPLATE.copy()

    for name, value in data["cookie"]:
        if name not in cookie_payload and name.isdigit(): # Add the session value to the machine-unique key
            cookie_payload["token"]["value"] = value
        else:
            cookie_payload[name]["value"] = value

    session["cookies"] = cookie_payload # Save the completed injection payload to the current session
    return jsonify({})

@mod.route("/schedule", methods=['GET'])
@requires_login
def schedule():
    """
    /webadvisor/schedule
    Gets the current semester's schedule from WebAdvisor
    """
    schedule = None

    with Navigator(session["cookies"]) as wd:
        # wd.inject_session(session["cookies"])
        wd.class_schedule("W16")
        schedule = wd.execute_script(constants.JS_SCRIPTS["class_schedule_extractor"])

    if schedule:
        print("Got schedule\n" + str(schedule))
        return jsonify(schedule) # Run the parser script on the page and return the script's result
    else:
        abort(500)

    # return send_file(io.BytesIO(wd.get_screenshot_as_png()), attachment_filename='logo.png', mimetype='image/png')

@mod.route("/<path>", methods=['GET'])
def error_viewer(path):
    return send_file("../" + path, mimetype='image/png')
