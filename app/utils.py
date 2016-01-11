from selenium import webdriver
from selenium.webdriver.support.ui import Select
from json import dumps as json_dumps

class PhantomDriver(webdriver.PhantomJS):
    """
    Custom Selenium WebDriver so that nicer API functions can be written if desired
    """
    def __init__(self):
        """
        Construct a new PhantomDriver object. Just calls the PhantomJS constructor
        """
        webdriver.PhantomJS.__init__(self, service_args= ["--load-images=false"])

    def find_elements_by_selector(self, selector):
        """
        Wrapper for find_elements_by_css_selector.

        :param selector: Valid CSS selector for the element
        :return: Returns either a list of elements, or if only one exists the single element. If any elements are <select> tags they are converted to Selenium Select objects
        """

        elements = [el if el.tag_name != "select" else Select(el) for el in self.find_elements_by_css_selector(selector)] # Convert any <select> tags
        if len(elements) == 1:
            return elements[0]

        return elements

def to_json(data):
    """
    More clear interface for json_dumps
    :return: JSON string
    """
    return json_dumps(data, separators=(',',':'))
