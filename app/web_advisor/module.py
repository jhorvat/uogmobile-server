import io
from functools import wraps
from flask import Blueprint, request, send_file, g, abort
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
        Fill the login form before moving on to the actual request
        """
        wd = g.get("wd", None)

        if not wd:
            abort(500)

        wd.get("https://webadvisor.uoguelph.ca/WebAdvisor/WebAdvisor?CONSTITUENCY=WBDF&type=P&pid=UT-LGRQ&PROCESS=-UTAUTH01") # Login to WebAdvisor
        wd.find_elements_by_selector("#USER_NAME").send_keys(app.config["USER_NAME"])
        wd.find_elements_by_selector("#CURR_PWD").send_keys(app.config["PASSWORD"])
        wd.find_elements_by_selector("#content > div.screen.UTAUTH01 > form").submit()
        print "Logged in"

        return f(*args, **kwargs)
    return decorated_function

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
    print "Fetched term select"
    wd.find_elements_by_selector("#VAR4").select_by_value("W16")
    wd.find_elements_by_selector("#content > div.screen.WESTS13A > form").submit()

    return to_json(wd.execute_script(constants.JS_SCRIPTS["class_schedule_extractor"])) # Run the parser script on the page and return the script's result

    # return send_file(io.BytesIO(wd.get_screenshot_as_png()), attachment_filename='logo.png', mimetype='image/png')
