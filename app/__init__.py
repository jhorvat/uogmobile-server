from flask import Flask, jsonify
from app.web_advisor.module import mod as web_advisor_module
from .api_error import ApiError

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(web_advisor_module)

@app.errorhandler(ApiError)
def handle_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
