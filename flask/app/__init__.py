from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from .course import course
from .invalid import *

app = Flask(__name__)
api = Api(app, prefix="/cutimetable/v1")
limiter = Limiter(app, key_func=get_remote_address, default_limits=["2 per 5 second"])
app.config["JSON_SORT_KEYS"] = False
app.config["JSON_AS_ASCII"] = False
# app.register_blueprint(course.bp, url_prefix="/cutimetable/v1")

course.Course.method_decorators.append(limiter.limit("10 per minute"))
api.add_resource(course.Course, "/course/<string:id>")


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
