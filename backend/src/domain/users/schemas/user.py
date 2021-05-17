from datetime import datetime
from uuid import uuid4

from flask import current_app
from marshmallow import Schema, fields, post_load, validate
from werkzeug.exceptions import HTTPException

from domain.users.entities.group import UserPositionEntity, GroupType
from domain.users.entities.user import UserEntity
from domain.users.schemas.contact import ContactSchema
from domain.users.schemas.group import GroupSchema, PositionGroupTypeEntitySchema


class UserValidationError(HTTPException):
    code = 400


class UserPositionSchema(Schema):
    __model__ = UserPositionEntity
    uuid = fields.Str(missing=lambda: str(uuid4()))
    position_id = fields.Str(required=True, dump_only=True)
    position = fields.Nested(PositionGroupTypeEntitySchema, dump_only=True)
    group_id = fields.Str(required=True, dump_only=True)
    group = fields.Nested(GroupSchema, dump_only=True)


class UserSchema(Schema):
    __model__ = UserEntity

    uuid = fields.Str(missing=lambda: str(uuid4()))
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Str(required=True)
    position_id = fields.Str(required=True)
    group_id = fields.Str(required=True, load_only=True)
    group_type = fields.Str(validate=validate.OneOf([e.value for e in GroupType]))
    position = fields.Nested("UserPositionSchema",  dump_only=True)
    contacts = fields.Nested(ContactSchema, many=True, dump_only=True)
    created_at = fields.DateTime(missing=lambda: datetime.utcnow())
    updated_at = fields.DateTime(missing=lambda: datetime.utcnow())

    @post_load
    def make_user(self, data: dict, **kwargs):
        return UserEntity.from_dict(data)

    def handle_error(self, exc, data, **kwargs):
        raise UserValidationError(description=exc.normalized_messages())


