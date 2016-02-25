from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from flask import current_app as app

from ..api_error import ApiError

class Navigator(webdriver.Remote):
    """
    PhantomDriver wrapper class to abstract away WebAdvisor URLs and other nitty-gritty like injecting the session
    """
    WEB_ADVISOR_URL = "https://webadvisor.uoguelph.ca/WebAdvisor/WebAdvisor"
    LOGIN_URL = "{}?CONSTITUENCY=WBDF&type=P&pid=UT-LGRQ&PROCESS=-UTAUTH01".format(WEB_ADVISOR_URL)
    CLASS_SCHEDULE_URL = "{}?CONSTITUENCY=WBST&type=P&pid=ST-WESTS13A".format(WEB_ADVISOR_URL)

    __cookies__ = None

    def __init__(self, cookies):
        """
        Super init and then navigate to the login page since we always want there to be a page immediately
        """
        # options = ChromeOptions()
        # # TODO: Want to add this but might have to create custom selenium containers to do it
        # options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

        super(Navigator, self).__init__(
            command_executor='http://hub:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.FIREFOX
            # desired_capabilities=DesiredCapabilities.CHROME
            # desired_capabilities=options.to_capabilities()
        )
        self.__cookies__ = cookies

    def __enter__(self):
        self.__inject_session__(self.__cookies__)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.quit()

        if exc_type is not None:
            raise ApiError("Driver exited with error", cause=exc_type, status_code=500 if isinstance(exc_type, TimeoutException) else 403)

    def __inject_session__(self, cookie_payload):
        """
        Injects a session payload into the WebDriver instance
        """
        self.login_page()

        for cookie in self.get_cookies():
            """
            WebAdvisor sets a unique name for the session cookie based on the machine so we MUST preserve that, however the session
            info itself isn't cross-referenced so as long as the cookie name and value match indepently we're good
            """
            if cookie["name"].isdigit():
                cookie_payload["token"]["name"] = cookie["name"]

        self.delete_all_cookies()

        for _, cookie in cookie_payload.items(): # There's no bulk cookie addition so add each one individually
            try:
                if cookie["value"]:
                    self.add_cookie(cookie)
            except Exception as e:
                pass

    def login_page(self):
        self.get(self.LOGIN_URL)

    def class_schedule(self, term):
        self.get(self.CLASS_SCHEDULE_URL) # Select the current semester

        self.find_elements_by_selector("#VAR4").select_by_value(term)
        self.find_elements_by_selector("#content > div.screen.WESTS13A > form").submit()
        self.wait_for_selector("#GROUP_Grp_LIST_VAR6 > table")

    def wait_for_selector(self, selector):
        WebDriverWait(self, 15, poll_frequency=0.1).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
        )

    def find_elements_by_selector(self, selector):
        """
        Wrapper for find_elements_by_css_selector.

        :param selector: Valid CSS selector for the element
        :return: Returns either a list of elements, or if only one exists the single element. If any elements are <select> tags they are converted to Selenium Select objects
        """
        find = lambda s: [el if el.tag_name != "select" else Select(el) for el in self.find_elements_by_css_selector(s)] # Convert any <select> tags

        self.wait_for_selector(selector)
        elements = find(selector)

        if len(elements) == 1:
            return elements[0]

        return elements
