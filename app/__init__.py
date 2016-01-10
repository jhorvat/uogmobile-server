from flask import Flask

app = Flask(__name__)

from app.web_advisor.module import mod as web_advisor_module
app.register_blueprint(web_advisor_module)
