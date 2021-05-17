from __future__ import annotations
from uuid import uuid4

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Union, List, Optional

from dataclasses_json import dataclass_json
from werkzeug.exceptions import HTTPException

from domain.core.entity import Entity
from domain.evenements.entities.reaction_entity import ReactionEntity, ReactionType
from domain.evenements.entities.resource import ResourceEntity
from domain.evenements.entities.tag_entity import TagEntity
from domain.users.entities.group import GroupEntity
from domain.users.entities.user import UserEntity


class NotFoundResourceInThisMessage(HTTPException):
    code = 404
    description = "Resource not found in this message"


class TagAlreadyInThisMessage(HTTPException):
    code = 409
    description = "Tag already exists in this message"


class ReactionAlreadyExistsOnThisMessage(HTTPException):
    code = 409
    description = "Reaction already exists in this message"


class ReactionNotFoundOnThisMessage(HTTPException):
    code = 404
    description = "Reaction not found in this message"


class NotFoundTagInThisMessage(HTTPException):
    code = 404
    description = "Tag not found in this message"


class Severity(Enum):
    EXTREME = 1
    SEVERE = 2
    MODERATE = 3
    MINOR = 4
    UNKNOWN = 5


class MessageType(str, Enum):
    INFORMATION = "info"
    ASK = "ask"
    DO = "do"
    NEED_INFO = "need_info"
    AFFAIR = "affair"
    MEETING = "meeting"
    UNKNOWN = "unknown"

    def __str__(self):
        return self.value

    @staticmethod
    def get_mapping() -> dict:
        return {
            "info": "Information",
            "ask": "Demande",
            "affair": "Intervention",
            "meeting": "Conversation vidéo"
        }

    @staticmethod
    def get_label(message_type) -> str:
        return MessageType.get_mapping().get(message_type, "Message")


@dataclass_json
@dataclass
class MessageEntity(Entity):
    title: str
    creator_id: str
    description: Optional[str] = field(default_factory=lambda: None)
    creator_id: Optional[str] = field(default_factory=lambda: None)
    external_id: Optional[str] = field(default_factory=lambda: None)
    creator: Optional[UserEntity] = field(default_factory=lambda: None)
    severity: Severity = field(default_factory=lambda: Severity.UNKNOWN)
    started_at: Optional[datetime] = field(default_factory=lambda: None)
    tags: List[TagEntity] = field(default_factory=lambda: [])
    resources: List[ResourceEntity] = field(default_factory=lambda: [])
    reactions: List[ReactionEntity] = field(default_factory=lambda: [])
    created_at: datetime = field(default_factory=lambda: datetime.now())
    updated_at: datetime = field(default_factory=lambda: datetime.now())
    type: MessageType = field(default_factory=lambda: MessageType.UNKNOWN)
    parent_id: Optional[str] = field(default_factory=lambda: None)
    parent: Optional[MessageEntity] = field(default_factory=lambda: None)
    executor_id: Optional[str] = field(default_factory=lambda: None)
    done_at: Optional[datetime] = field(default_factory=lambda: None)
    restricted_to: List[GroupEntity] = field(default_factory=lambda: [])
    restricted_to_group_ids: List[str] = field(default_factory=lambda: [])

    def __eq__(self, other):
        return self.uuid == other.uuid

    @classmethod
    def from_affair(cls, affair):
        return cls(
            uuid=str(uuid4()),
            external_id=affair.uuid,
            description=affair.affair["eventLocation"]["address"],
            title=affair.affair["primaryAlert"]["alertCode"]["whatsHappen"]["label"],
            created_at=affair.created_at,
            type=MessageType.AFFAIR
        )

    @classmethod
    def from_meeting(cls, meeting):
        return cls(
            uuid=str(uuid4()),
            external_id=meeting.uuid,
            description=f"{meeting.link}",
            title="Cliquez pour rejoindre la réunion vidéo",
            started_at=meeting.created_at,
            created_at=meeting.created_at,
            updated_at=meeting.updated_at,
            type=MessageType.MEETING
        )

    def add_parent_message(self, message: MessageEntity):
        self.parent_message_id = message.uuid
        self.parent_message = message

    def add_tag(self, tag: TagEntity) -> TagEntity:
        try:
            self.get_tag_by_id(uuid=tag.uuid)
            raise TagAlreadyInThisMessage()
        except NotFoundTagInThisMessage:
            self.tags.append(tag)
            return tag

    def remove_tag(self, tag: TagEntity) -> TagEntity:
        self.get_tag_by_id(uuid=tag.uuid)
        self.tags.remove(tag)
        return tag

    def get_tags(self) -> List[TagEntity]:
        return self.tags

    def get_tag_by_id(self, uuid: str) -> TagEntity:
        matches = [tag for tag in self.tags if tag.uuid == uuid]
        if not matches:
            raise NotFoundTagInThisMessage()
        return matches[0]

    def add_resource(self, resource: ResourceEntity) -> ResourceEntity:
        self.resources.append(resource)
        resource.set_message_id(self.uuid)
        return resource

    def remove_resource(self, resource: ResourceEntity) -> ResourceEntity:
        self.resources.remove(resource)
        resource.reset_message_id()
        return resource

    def get_resources(self):
        return self.resources

    def get_resource_by_id(self, uuid: str) -> ResourceEntity:
        matches = [resource for resource in self.resources if resource.uuid == uuid]
        if not matches:
            raise NotFoundResourceInThisMessage()
        return matches[0]

    def set_creator(self, user: UserEntity):
        self.creator = user

    def is_authorized_to_modify(self, user_uuid) -> bool:
        return self.creator_id == user_uuid

    def get_reactions(self):
        return self.reactions

    def get_reaction_by_id(self, creator_id: str, reaction_type: ReactionType) -> Optional[ReactionEntity]:
        for reaction in self.reactions:
            if reaction.creator_id == creator_id and reaction.type == reaction_type:
                return reaction
        raise ReactionNotFoundOnThisMessage()

    def add_reaction(self, reaction: ReactionEntity) -> ReactionEntity:
        try:
            if self.get_reaction_by_creator_id(creator_id=reaction.creator_id, type=reaction.type):
                raise ReactionAlreadyExistsOnThisMessage()
        except NotFoundTagInThisMessage:
            self.reactions.append(reaction)
            return reaction

    def remove_reaction(self, reaction: ReactionEntity) -> ReactionEntity:
        reaction = self.get_reaction_by_creator_id(creator_id=reaction.creator_id, type=reaction.type)
        self.reactions.remove(reaction)
        return reaction

    def add_group_restriction(self, group: GroupEntity):
        self.restricted_to.append(group)

    def remove_group_restriction(self, group: GroupEntity):
        self.restricted_to.remove(group)
