from flask import Blueprint, make_response, jsonify, g, current_app
from flask_restful import Api, request

from entrypoints.middleware import user_info_middleware

enki_blueprint = Blueprint(name="enki_blueprint", import_name=__name__, url_prefix="/api/enki")
api = Api(enki_blueprint)


@enki_blueprint.route('/', methods=["GET"])
@user_info_middleware
def hello_enki():
    response = make_response(jsonify({
        'message': 'Hello, Enki!',
        "info": g.user_info,
    }))
    return response
