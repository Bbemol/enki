import logging

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from sqlalchemy.orm import clear_mappers

from adapters.postgres.base_orm import start_mappers
from entrypoints import views
from service_layer.messagebus import HANDLERS
from .commands import seeds
from .config import EnkiConfig
from .errors import errors
from .extensions import event_bus, api_spec

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)


def register_blueprints(app: Flask):
    """
    Register blueprints
    :param app:
    :return:
    """
    app.register_blueprint(views.hello_page_blueprint)
    app.register_blueprint(views.enki_blueprint)
    app.register_blueprint(views.enki.enki_blueprint_v1)
    app.register_blueprint(views.core_blueprint)
    app.register_blueprint(views.echanges_blueprint)


def configure_apispec(app):
    """Configure APISpec for swagger support
    """
    api_spec.init_app(app)
    api_spec.spec.components.security_scheme("jwt", {
        "type": "openIdConnect",
        "flows": {
            "implicit": {
                "authorizationUrl": "http://keycloak:8080/auth/realms/enki/protocol/openid-connect/auth",
                "clientId": "angular_frontend"
            }
        },
        "bearerFormat": "bearer",
        "openIdConnectUrl": "http://keycloak:8080/auth/realms/enki/.well-known/openid-configuration",
    })


def create_app(testing=False):
    """

    :return:
    """
    app = Flask('enki')
    app.config.from_object(EnkiConfig)
    CORS(app)

    if testing is True:
        app.config["TESTING"] = True

    api = Api(app, errors=errors)
    context = app.config["CONTEXT_FACTORY"](config=EnkiConfig())
    configure_event_bus(context=context)
    context.init_app(app=app)
    configure_apispec(app=app)
    register_blueprints(app)
    register_cli_commands(app=app)
    configure_orm()
    return app


def register_cli_commands(app):
    app.cli.add_command(seeds.create_group_and_locations)
    app.cli.add_command(seeds.create_position_group)
    app.cli.add_command(seeds.create_affairs)
    app.cli.add_command(seeds.create_sdis_groups)
    app.cli.add_command(seeds.create_custom_group)


def configure_redoc(app):
    app.config['REDOC'] = {
        'endpoint': 'docs',
        'spec_route': '/docs',
        'static_url_path': '/redoc_static',
        'title': 'ReDoc',
        'version': '1.0.0',
        'openapi_version': '3.0.2',
        'info': dict(),
        'marshmallow_schemas': list()
    }
    redoc = Redoc(app)


def configure_orm():
    clear_mappers()
    start_mappers()


def configure_event_bus(context):
    for topic, callbacks in HANDLERS.items():
        for callback in callbacks:
            event_bus.subscribe(topic=topic, callback=callback)


app = create_app()
