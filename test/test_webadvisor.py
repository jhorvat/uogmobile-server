import unittest
import json
from app import app

class WebAdvisorTestCase(unittest.TestCase):
    OLD_COOKIE = "__utmc=126958603**; __utmb=126958603**; __utma=126958603.996207414.1456255983.1456255983.1456255983.1**; 474041339=8317232852*N*313364915054037; __utmz=126958603.1456255983.1.1.utmccn**; LASTTOKEN=474041339; survey=N%3A474041339; __utma=126958603.996207414.1456255983.1456255983.1456255983.1; __utmc=126958603; __utmz=126958603.1456255983.1.1.utmccn=(direct)|utmcsr=(direct)|utmcmd=(none); __utmb=126958603**"

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = "Testing Secret!"
        self.app = app.test_client()

    def login(self, cookie):
        return self.app.post("/webadvisor/login", headers=[('Content-Type', 'application/json')], data=json.dumps({
            "cookie": cookie
        }))

    def test_login_cookie_parse(self):
        self.assertEqual(self.login(self.OLD_COOKIE).status_code, 200)

    def test_get_schedule(self):
        cookie = input("Give me a valid WebAdvisor cookie: ")
        login = self.login(cookie)
        self.assertEqual(login.status_code, 200)

        schedule = self.app.get("/webadvisor/schedule")
        self.assertEqual(schedule.status_code, 200)

        data = json.loads(schedule.get_data().decode("UTF8"))
        self.assertIn("courses", data)

    def test_get_schedule_bad_cookie(self):
        login = self.login(self.OLD_COOKIE)
        self.assertEqual(login.status_code, 200)

        schedule = self.app.get("/webadvisor/schedule")
        data = json.loads(schedule.get_data().decode("UTF8"))
        print(data)
