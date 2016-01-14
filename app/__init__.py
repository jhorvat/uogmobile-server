from flask import Flask
from app.web_advisor.module import mod as web_advisor_module

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(web_advisor_module)
