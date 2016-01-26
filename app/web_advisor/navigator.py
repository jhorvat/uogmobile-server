from app.utils import PhantomDriver

class Navigator(PhantomDriver):
    _web_advisor_url = "https://webadvisor.uoguelph.ca/WebAdvisor/WebAdvisor"
    _login_url = "{}?CONSTITUENCY=WBDF&type=P&pid=UT-LGRQ&PROCESS=-UTAUTH01".format(_web_advisor_url)
    _class_schedule_url = "{}?CONSTITUENCY=WBST&type=P&pid=ST-WESTS13A".format(_web_advisor_url)

    def __init__(self):
        super(Navigator, self).__init__()
        self.login_page()

    def login_page(self):
        self.get(_login_url)

    def class_schedule(self):
        self.get(_class_schedule_url) # Select the current semester

    def inject_session(self, cookie_payload):
        for cookie in self.get_cookies():
            """
            WebAdvisor sets a unique name for the session cookie based on the machine so we MUST preserve that, however the session
            info itself isn't cross-referenced so as long as the cookie name and value match indepently we're good
            """
            if cookie["name"].isdigit():
                cookie_payload["token"]["name"] = cookie["name"]

        self.delete_all_cookies()
        map(lambda (k, v): self.add_cookie(v), cookie_payload.iteritems())
