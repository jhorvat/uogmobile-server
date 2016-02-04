from app.utils import PhantomDriver

class Navigator(PhantomDriver):
    """
    PhantomDriver wrapper class to abstract away WebAdvisor URLs and other nitty-gritty like injecting the session
    """
    _web_advisor_url = "https://webadvisor.uoguelph.ca/WebAdvisor/WebAdvisor"
    _login_url = "{}?CONSTITUENCY=WBDF&type=P&pid=UT-LGRQ&PROCESS=-UTAUTH01".format(_web_advisor_url)
    _class_schedule_url = "{}?CONSTITUENCY=WBST&type=P&pid=ST-WESTS13A".format(_web_advisor_url)

    def __init__(self):
        """
        Super init and then navigate to the login page since we always want there to be a page immediately
        """
        super(Navigator, self).__init__()
        print("Init super")
        self.login_page()
        print("Loaded page")

    def login_page(self):
        self.get(self._login_url)

    def class_schedule(self):
        self.get(self._class_schedule_url) # Select the current semester

    def inject_session(self, cookie_payload):
        """
        Injects a session payload into the WebDriver instance
        """
        for cookie in self.get_cookies():
            """
            WebAdvisor sets a unique name for the session cookie based on the machine so we MUST preserve that, however the session
            info itself isn't cross-referenced so as long as the cookie name and value match indepently we're good
            """
            if cookie["name"].isdigit():
                cookie_payload["token"]["name"] = cookie["name"]

        self.delete_all_cookies()

        for _, cookie in cookie_payload.items(): # There's no bulk cookie addition so add each one individually
            self.add_cookie(cookie)
