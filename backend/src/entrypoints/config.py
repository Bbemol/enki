import os
from typing import Optional

from service_layer.unit_of_work import AbstractUnitOfWork, SqlAlchemyUnitOfWork
from .serializers import EnkiJsonEncoder


class EnkiConfig(object):
    RESTFUL_JSON = {
        'indent': 2,
        'cls': EnkiJsonEncoder
    }
    SGE_HUB_BASE_URI: str = os.environ.get('SGE_HUB_BASE_URI',
                                           'http://docker.for.mac.localhost:9090')
    SGE_REF_BASE_URI: str = os.environ.get('SGE_REF_BASE_URI',
                                           'http://docker.for.mac.localhost:10010')
    DATABASE_URI: str = os.environ.get("DATABASE_URI", "sqlite:///:memory:")
    ENKI_SGE_ID = "sgc-enki"
    ENKI_SGE_ADDRESS = "sge:sgc-enki"
    AFFAIR_REPOSITORY = os.environ.get("AFFAIR_REPOSITORY")
    CONTEXT_FACTORY: AbstractUnitOfWork = SqlAlchemyUnitOfWork
    TWILIO_ACCOUNT_SID: Optional[str] = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN: Optional[str] = os.environ.get('TWILIO_AUTH_TOKEN')
    FROM_EMAIL = "enki@ansc.fr"
    FROM_TEL_NUMBER = "+13345084085"
    TO_TEL_NUMBER = "+33772324157"
    ENKI_FRONT_BASE_URI: str = os.environ.get(
        'ENKI_FRONT_BASE_URI',
        'http://localhost:4200'
    )

    ELASTIC_HOST = os.environ.get('ELASTIC_USER', "http://elasticsearch:9200")
    ELASTIC_USER = os.environ.get('ELASTIC_HOST', "elastic")
    ELASTIC_PASSWORD = os.environ.get('ELASTIC_PASSWORD', "changeme")

    ## Athentication

    SECRET_KEY = 'SomethingNotEntirelySecret'

    ##
    API_URL = "http://localhost:5000"

    # MINIO
    MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT", "minio")
    MINIO_PORT = os.environ.get("MINIO_PORT", "9000")
    MINIO_URI = os.environ.get("MINIO_URI", f"{MINIO_ENDPOINT}:{MINIO_PORT}")
    
    MINIO_MESSAGE_RESOURCES_BUCKET = os.environ.get("MINIO_MESSAGE_RESOURCES_BUCKET", "messages-test")
    MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY", "MINIOACCESSKEY")
    MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY", "MINIO_SECRET_KEY")
    MINIO_REGION = os.environ.get("MINIO_REGION", "fr-par")
    MINIO_SECURE = os.environ.get("MINIO_SECURE", "false") == "true"

    KEYCLOAK_BASE_URL = os.environ.get("KEYCLOAK_BASE_URL")
    KEYCLOAK_REALM = os.environ.get("KEYCLOAK_REALM")
    KEYCLOAK_USERNAME = os.environ.get("KEYCLOAK_USERNAME")
    KEYCLOAK_PASSWORD = os.environ.get("KEYCLOAK_PASSWORD")

    EMAIL_HOST = os.environ.get("EMAIL_HOST")
    EMAIL_PORT = os.environ.get("EMAIL_PORT")
    EMAIL_USER = os.environ.get("EMAIL_USER")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
