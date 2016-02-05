from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
from json import dumps as json_dumps
from json import loads as from_json

class PhantomDriver(webdriver.Remote):
    """
    Custom Selenium WebDriver so that nicer API functions can be written if desired
    """
    def __init__(self):
        """
        Construct a new PhantomDriver object. Just calls the PhantomJS constructor
        """
        # webdriver.PhantomJS.__init__(self, service_args= ["--load-images=false"])
        super(PhantomDriver, self).__init__(command_executor='http://localhost:4444/wd/hub', desired_capabilities=DesiredCapabilities.PHANTOMJS)
        # super(PhantomDriver, self).__init__(command_executor='http://localhost:8910', desired_capabilities=DesiredCapabilities.PHANTOMJS)

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

def to_json(data):
    """
    More clear interface for json_dumps
    :return: JSON string
    """
    return json_dumps(data, separators=(',',':'))
