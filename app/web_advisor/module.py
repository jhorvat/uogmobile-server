import io
from functools import wraps
from flask import Blueprint, request, session, send_file, g, abort, jsonify
from flask import current_app as app

import constants
from app.utils import to_json
from navigator import Navigator

# TODO: Migrate to WebDriver to context manager maybe
mod = Blueprint('web_advisor', __name__, url_prefix="/webadvisor")

@mod.before_request
def before_request():
    """
    Preflight request setup
    """
    g.wd = Navigator() # Get a PhantomJS session and load it into the request context

@mod.teardown_request
def teardown_request(exception):
    """
    Postflight request cleanup
    """
    wd = g.get("wd", None) # Make sure to close the session
    if not wd:
        wd.close()

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

    if data["cookie"]:
        # Separate the cookies string into a list of key, value tuples
        data["cookie"] = [cookie.split("=", 1) for cookie in data["cookie"].replace(" ", "").split(";")]
    else:
        abort(400)

    wd = g.get("wd", None)
    cookie_payload = constants.WEB_ADVISOR_COOKIES_TEMPLATE()

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
@requires_login
def schedule():
    """
    /webadvisor/schedule
    Gets the current semester's schedule from WebAdvisor
    """
    wd = g.get("wd", None)

    if not wd:
        abort(500)

    wd.class_schedule()
    wd.find_elements_by_selector("#VAR4").select_by_value("W16")
    wd.find_elements_by_selector("#content > div.screen.WESTS13A > form").submit()

    return jsonify(wd.execute_script(constants.JS_SCRIPTS["class_schedule_extractor"])) # Run the parser script on the page and return the script's result
    # return send_file(io.BytesIO(wd.get_screenshot_as_png()), attachment_filename='logo.png', mimetype='image/png')
