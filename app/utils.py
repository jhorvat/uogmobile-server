from selenium import webdriver
from selenium.webdriver.support.ui import Select
from json import dumps as json_dumps

class PhantomDriver(webdriver.PhantomJS):
    def __init__(self):
        webdriver.PhantomJS.__init__(self, service_args= ["--load-images=false"])

    def find_elements_by_selector(self, selector):
        elements = [el if el.tag_name != "select" else Select(el) for el in self.find_elements_by_css_selector(selector)]
        if len(elements) == 1:
            return elements[0]

        return elements

def to_json(data):
    return json_dumps(data, separators=(',',':'))
