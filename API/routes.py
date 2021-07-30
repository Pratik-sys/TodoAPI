from flask import jsonify, request
from flask_restx import Resource
from API import api
from API.models import User
from datetime import date as D


@api.route("/list")
class GetData(Resource):
    def get(self):
        data = User.objects(name="gulshan").first()
        return jsonify(data)
