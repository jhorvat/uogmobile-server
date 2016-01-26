JS_SCRIPTS = {}

# Store this as a function so that we always get a fresh template of the cookie payload
WEB_ADVISOR_COOKIES_TEMPLATE = lambda: {
    "token": {
        "name": None,
        "value": None,
        "path": "/WebAdvisor",
        "domain": "webadvisor.uoguelph.ca"
    },
    "LASTTOKEN": {
        "name": "LASTTOKEN",
        "value": None,
        "path": "/WebAdvisor",
        "domain": "webadvisor.uoguelph.ca"
    },
    "__utma": {
        "name": "__utma",
        "value": None,
        "path": "/WebAdvisor",
        "domain": "webadvisor.uoguelph.ca"
    },
    "__utma_prime": {
        "name": "__utma",
        "value": None,
        "path": "/",
        "domain": ".webadvisor.uoguelph.ca"
    },
    "__utmb": {
        "name": "__utmb",
        "value": None,
        "path": "/WebAdvisor",
        "domain": "webadvisor.uoguelph.ca"
    },
    "__utmb_prime": {
        "name": "__utmb",
        "value": None,
        "path": "/",
        "domain": ".webadvisor.uoguelph.ca"
    },
    "__utmc": {
        "name": "__utmc",
        "value": None,
        "path": "/WebAdvisor",
        "domain": "webadvisor.uoguelph.ca"
    },
    "__utmc_prime": {
        "name": "__utmc",
        "value": None,
        "path": "/",
        "domain": ".webadvisor.uoguelph.ca"
    },
    "__utmz": {
        "name": "__utmz",
        "value": None,
        "path": "/WebAdvisor",
        "domain": "webadvisor.uoguelph.ca"
    },
    "__utmz_prime": {
        "name": "__utmz",
        "value": None,
        "path": "/",
        "domain": ".webadvisor.uoguelph.ca"
    },
    "survey": {
        "name": "survey",
        "value": None,
        "path": "/WebAdvisor",
        "domain": "webadvisor.uoguelph.ca"
    }
}
