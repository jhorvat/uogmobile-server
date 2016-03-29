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
    WebDriver wrapper class to abstract away Central lookup
    """
    DIRECTORY_URL = "http://www.uoguelph.ca/directory/index.cfm?search=complex"

    def __init__(self):
        """
        Super init and then navigate to the login page since we always want there to be a page immediately
        """

        super(Navigator, self).__init__(
            command_executor='http://hub:4444/wd/hub',
            # desired_capabilities=DesiredCapabilities.FIREFOX
            desired_capabilities=DesiredCapabilities.CHROME
            # desired_capabilities=options.to_capabilities()
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.quit()

        if exc_type is not None:
            raise ApiError("Driver exited with error", cause=exc_type, status_code=500 if isinstance(exc_type, TimeoutException) else 403)

    def lookup_student(self, email):
        self.get(self.DIRECTORY_URL)

        self.find_elements_by_selector("#main-column > table > tbody > tr > td > form > fieldset > div:nth-child(5) > input") \
            .send_keys(email)

        self.find_elements_by_selector('#main-column > table > tbody > tr > td > form > fieldset > input[type="submit"]:nth-child(15)') \
            .click()

        search_result_header = self.find_elements_by_selector("#main-column > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(1) > td")

        return None \
            if "Found 1 record" not in search_result_header.text else \
            self.find_elements_by_selector("#main-column > table > tbody > tr:nth-child(2) > td > table > tbody > tr.vcard > td > span.fn") .text

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
