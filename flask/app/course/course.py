from flask import Blueprint, request, abort, jsonify
from flask_restful import Resource
from ..constant import *
from .validate import *
from .regchula_services import *

import requests
import json


# bp = Blueprint("course", __name__)


class Course(Resource):

    # @bp.route("/courses/<string:id>", methods=["GET"])
    def get(self, id):

        year = intTryParse(request.args.get("year", default=defaultYear()))
        sem = intTryParse(request.args.get("sem", default=defaultSem()))

        validateIdYearSem(id, year, sem)
        course = getCourse(id, year[0], sem[0])

        # return json.dumps(course, ensure_ascii=False)
        response = jsonify(course[0])
        response.status_code = course[1]
        return response
