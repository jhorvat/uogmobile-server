from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class Navigator(webdriver.Remote):
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
        super(Navigator, self).__init__(command_executor='http://localhost:4444/wd/hub', desired_capabilities=DesiredCapabilities.PHANTOMJS)

    def __enter__(self):
        self.login_page()
        WebDriverWait(self, 30, poll_frequency=0.1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#content > div.screen.UTAUTH01 > form"))
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print("Driver exited with error!")

        self.quit()

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
                print("Unique ID is " + cookie["name"])
                cookie_payload["token"]["name"] = cookie["name"]

        self.delete_all_cookies()

        for _, cookie in cookie_payload.items(): # There's no bulk cookie addition so add each one individually
            try:
                self.add_cookie(cookie)
            except:
                print("Failed to set cookie\n" + str(cookie))

    def find_elements_by_selector(self, selector):
        """
        Wrapper for find_elements_by_css_selector.

        :param selector: Valid CSS selector for the element
        :return: Returns either a list of elements, or if only one exists the single element. If any elements are <select> tags they are converted to Selenium Select objects
        """

        elements = [el if el.tag_name != "select" else Select(el) for el in self.find_elements_by_css_selector(selector)] # Convert any <select> tags
        if len(elements) == 1:
            return elements[0]

        print(elements)
        return elements
