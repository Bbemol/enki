from datetime import datetime
from uuid import uuid4

from flask import current_app
from marshmallow import Schema, fields, post_load, validate
from marshmallow_enum import EnumField
from werkzeug.exceptions import HTTPException
from domain.evenements.entities.evenement_type import EvenementType
from domain.evenements.entities.evenement_entity import EvenementEntity, EvenementRoleType, \
    UserEvenementRole

from domain.users.schemas.group import LocationSchema
from domain.users.schemas.user import UserSchema


class EvenementValidationError(HTTPException):
    code = 400


class UserEvenementRoleSchema(Schema):
    __model__ = UserEvenementRole

    uuid = fields.Str(missing=lambda: str(uuid4()))
    user_id = fields.Str(required=True)
    user = fields.Nested(UserSchema, dump_only=True)
    evenement_id = fields.Str(required=True)
    type = EnumField(EvenementRoleType, required=True, by_value=True)
    revoked_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(missing=lambda: datetime.utcnow(), dump_only=True)
    updated_at = fields.DateTime(missing=lambda: datetime.utcnow(), dump_only=True)


class EvenementSchema(Schema):
    __model__ = EvenementEntity

    uuid = fields.Str(missing=lambda: str(uuid4()))
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    location_id = fields.Str(required=False)
    type = EnumField(EvenementType, required=True, by_value=True, validate=validate.OneOf([e for e in EvenementType]))
    started_at = fields.DateTime(required=True)
    closed = fields.Boolean(dump_only=True)
    creator_id = fields.Str(required=False, dump_only=True)
    creator = fields.Nested(UserSchema, required=False, dump_only=True)
    ended_at = fields.DateTime(required=False, dump_only=True)
    location = fields.Nested(LocationSchema, dump_only=True)
    # messages = fields.Nested("MessageSchema", many=True, dump_only=True)
    # affairs = fields.Nested("SimpleAffairSchema", many=True, dump_only=True)
    user_roles = fields.Nested(UserEvenementRoleSchema, many=True)
    created_at = fields.DateTime(missing=lambda: datetime.utcnow())
    updated_at = fields.DateTime(missing=lambda: datetime.utcnow())

    @post_load
    def make_event(self, data: dict, **kwargs):
        return EvenementEntity.from_dict(data)

    def handle_error(self, exc, data, **kwargs):
        raise EvenementValidationError(description=exc.normalized_messages())


