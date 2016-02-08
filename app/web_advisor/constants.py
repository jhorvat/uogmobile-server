JS_SCRIPTS = {}

# Store this as a function so that we always get a fresh template of the cookie payload
WEB_ADVISOR_COOKIES_TEMPLATE = {
    "token": {
        "name": None,
        "value": None,
        "path": "/WebAdvisor",
        "domain": "webadvisor.uoguelph.ca",
    },
    "LASTTOKEN": {
        "name": "LASTTOKEN",
        "value": None,
        "path": "/WebAdvisor",
        "domain": "webadvisor.uoguelph.ca",
    },
    "survey": {
        "name": "survey",
        "value": None,
        "path": "/WebAdvisor",
        "domain": "webadvisor.uoguelph.ca",
    }
}
