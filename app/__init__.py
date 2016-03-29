from flask import Flask, jsonify
from app.web_advisor.module import mod as web_advisor_module
from app.student_dir.module import mod as student_dir_module
from .api_error import ApiError

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(web_advisor_module)
app.register_blueprint(student_dir_module)

@app.errorhandler(ApiError)
def handle_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
