import io
from functools import wraps
from flask import Blueprint, request, session, send_file, g, abort, jsonify
from flask import current_app as app

from . import constants
from app.utils import to_json
from .navigator import Navigator

# TODO: Migrate to WebDriver to context manager maybe
mod = Blueprint('web_advisor', __name__, url_prefix="/webadvisor")

def requires_navigator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        g.wd = Navigator()
        return f(*args, **kwargs)
    return decorated_function


def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """
        Get the WebAdvisor cookie payload
        """
        wd = g.get("wd", None)

        if not wd:
            abort(500)

        if "cookies" not in session:
            abort(403)

        wd.inject_session(session["cookies"])

        return f(*args, **kwargs)
    return decorated_function

@mod.route("/login", methods=['POST'])
def login():
    data = request.get_json()

    print(str(data))
    if "cookie" in data and data["cookie"]:
        # Separate the cookies string into a list of key, value tuples
        data["cookie"] = [cookie.split("=", 1) for cookie in data["cookie"].replace(" ", "").split(";")]
    else:
        abort(400)

    cookie_payload = constants.WEB_ADVISOR_COOKIES_TEMPLATE.copy()

    for name, value in data["cookie"]:
        if name.startswith("__"):
            if name == "__utmb": # __utmb's value doesn't vary between its two instances
                cookie_payload["__utmb"]["value"] = value
                cookie_payload["__utmb_prime"]["value"] = value
            elif value.endswith("**"):
                cookie_payload[name]["value"] = value
            else:
                cookie_payload[name + "_prime"]["value"] = value
        elif name not in cookie_payload: # Add the session value to the machine-unique key
            cookie_payload["token"]["value"] = value
        else:
            cookie_payload[name]["value"] = value

    session["cookies"] = cookie_payload # Save the completed injection payload to the current session
    return jsonify({})

@mod.route("/schedule", methods=['GET'])
@requires_navigator
@requires_login
def schedule():
    """
    /webadvisor/schedule
    Gets the current semester's schedule from WebAdvisor
    """
    try:
        wd = g.get("wd", None)

        wd.class_schedule()
        wd.find_elements_by_selector("#VAR4").select_by_value("W16")
        wd.find_elements_by_selector("#content > div.screen.WESTS13A > form").submit()

        schedule = wd.execute_script(constants.JS_SCRIPTS["class_schedule_extractor"])
    except:
        wd.get_screenshot_as_file("error.png")
    finally:
        wd.quit()

        if schedule:
            return jsonify(schedule) # Run the parser script on the page and return the script's result
        else:
            abort(500)
    # return send_file(io.BytesIO(wd.get_screenshot_as_png()), attachment_filename='logo.png', mimetype='image/png')

@mod.route("/error", methods=['GET'])
def error_viewer():
    return send_file("../error.png", mimetype='image/png')
