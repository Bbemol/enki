from datetime import datetime
from uuid import uuid4

from marshmallow import Schema, fields, post_load
from werkzeug.exceptions import HTTPException

from domain.echanges.entities.echange_entity import EchangeEntity


class EchangeValidationError(HTTPException):
    code = 400


class EchangeSchema(Schema):
    __model__ = EchangeEntity
    uuid = fields.Str(missing=lambda: str(uuid4()))
    payload = fields.Str(required=True)
    created_at = fields.DateTime(missing=lambda: datetime.utcnow(), dump_only=True)

    @post_load
    def make_simple_echange(self, data: dict, **kwargs):
        return EchangeEntity.from_dict(data)

    def handle_error(self, exc, data, **kwargs):
        raise EchangeValidationError(description=exc.normalized_messages())
