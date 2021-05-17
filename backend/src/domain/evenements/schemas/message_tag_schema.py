from __future__ import annotations
from datetime import datetime
from uuid import uuid4

from flask import current_app
from marshmallow import Schema, fields, post_load, validate
from marshmallow_enum import EnumField
from werkzeug.exceptions import HTTPException

from domain.evenements.entities.message_entity import MessageEntity, MessageType, Severity
from domain.evenements.entities.tag_entity import TagEntity
from domain.evenements.schemas.resource_schema import ResourceSchema
from domain.evenements.schemas.reaction_schema import ReactionSchema
from domain.users.schemas.user import UserSchema


class MessageValidationError(HTTPException):
    code = 400


class TagValidationError(HTTPException):
    code = 400


class TagSchema(Schema):
    __model__ = TagEntity

    uuid = fields.Str(missing=lambda: str(uuid4()))
    title = fields.Str(required=True, validate=validate.Length(min=5))
    slug = fields.Str(dump_only=True)
    creator_id = fields.Str(required=False)
    created_at = fields.DateTime(missing=lambda: datetime.utcnow(), dump_only=True)
    updated_at = fields.DateTime(missing=lambda: datetime.utcnow(), dump_only=True)

    @post_load
    def make_tag(self, data: dict, **kwargs):
        return TagEntity.from_dict(data)

    def handle_error(self, exc, data, **kwargs):
        raise TagValidationError(description=exc.normalized_messages())


class MessageSchema(Schema):
    __model__ = MessageEntity

    uuid = fields.Str(missing=lambda: str(uuid4()))
    title = fields.Str(required=True, validate=validate.Length(min=2, max=150))
    description = fields.Str(required=False)
    severity = EnumField(Severity, missing=Severity.UNKNOWN, validate=validate.OneOf([e.value for e in Severity]))
    type = fields.Str(missing=MessageType.INFORMATION.value, validate=validate.OneOf([e.value for e in MessageType]))
    type_label = fields.Method("_build_type_label")
    creator_id = fields.Str(required=False, dump_only=True)
    creator = fields.Nested(UserSchema, dump_only=True)
    started_at = fields.DateTime(required=False)
    tags = fields.Nested(TagSchema, many=True, dump_only=True)
    parent = fields.Nested('MessageSchema', required=False, dump_only=True)
    parent_id = fields.Str(required=False, load_only=True)
    resources = fields.Nested(ResourceSchema, required=False, many=True, dump_only=True)
    executor_id = fields.Str(required=False)
    reactions = fields.Nested(ReactionSchema, required=False, many=True, dump_only=True)
    done_at = fields.DateTime(default=None, dump_only=True)
    restricted = fields.Method("_is_restricted")

    created_at = fields.DateTime(missing=lambda: datetime.now(), dump_only=True)
    updated_at = fields.DateTime(missing=lambda: datetime.now(), dump_only=True)

    @post_load
    def make_message(self, data: dict, **kwargs):
        entity = MessageEntity.from_dict(data)
        return entity

    def _build_type_label(self, obj) -> str:
        return MessageType.get_label(message_type=obj.type)

    def _is_restricted(self, obj) -> bool:
        if obj.restricted_to:
            return True
        else:
            return False

    def handle_error(self, exc, data, **kwargs):
        error_data = exc.normalized_messages()
        error_data["valid"] = [e for e in MessageType]
        raise MessageValidationError(description=error_data)

