import io
from functools import wraps
from flask import Blueprint, request, session, send_file, g, abort
from flask import current_app as app


import constants
from app.utils import to_json, PhantomDriver

mod = Blueprint('web_advisor', __name__, url_prefix="/webadvisor")

@mod.before_request
def before_request():
    """
    Preflight request setup
    """
    g.wd = PhantomDriver() # Get a PhantomJS session and load it into the request context

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
        cookie_payload = constants.WEB_ADVISOR_COOKIES_TEMPLATE()
        wd = g.get("wd", None)

        if not wd:
            abort(500)

        if "cookies" not in session:
            abort(403)

        wd.get("https://webadvisor.uoguelph.ca/WebAdvisor/WebAdvisor?CONSTITUENCY=WBDF&type=P&pid=UT-LGRQ&PROCESS=-UTAUTH01")
        for cookie in wd.get_cookies():
            """
            WebAdvisor sets a unique name for the session cookie based on the machine so we MUST preserve that, however the session
            info itself isn't cross-referenced so as long as the cookie name and value match indepently we're good
            """
            if cookie["name"].isdigit():
                cookie_payload["token"]["name"] = cookie["name"]

        for name, value in session["cookies"]:
            if name.startswith("__"):
                if name == "__utmb":
                    cookie_payload["__utmb"]["value"] = value
                    cookie_payload["__utmb_prime"]["value"] = value
                elif value.endswith("**"):
                    cookie_payload[name]["value"] = value
                else:
                    cookie_payload[name + "_prime"]["value"] = value
            elif name not in cookie_payload:
                cookie_payload["token"]["value"] = value
            else:
                cookie_payload[name]["value"] = value

        wd.delete_all_cookies()
        map(lambda (k, v): wd.add_cookie(v), cookie_payload.iteritems())

        return f(*args, **kwargs)
    return decorated_function

@mod.route("/login", methods=['POST'])
def login():
    data = request.get_json()

    if not data["cookie"]:
        abort(400)

    session["cookies"] = [cookie.split("=", 1) for cookie in data["cookie"].replace(" ", "").split(";")]
    return "Success"

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

    wd.get("https://webadvisor.uoguelph.ca/WebAdvisor/WebAdvisor?CONSTITUENCY=WBST&type=P&pid=ST-WESTS13A") # Select the current semester
    return send_file(io.BytesIO(wd.get_screenshot_as_png()), attachment_filename='logo.png', mimetype='image/png')
    # wd.find_elements_by_selector("#VAR4").select_by_value("W16")
    # wd.find_elements_by_selector("#content > div.screen.WESTS13A > form").submit()
    #
    # return to_json(wd.execute_script(constants.JS_SCRIPTS["class_schedule_extractor"])) # Run the parser script on the page and return the script's result
