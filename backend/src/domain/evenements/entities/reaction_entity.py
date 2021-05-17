from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from dataclasses_json import dataclass_json
from domain.core.entity import Entity
from domain.users.entities.user import UserEntity


class ReactionType(str, Enum):
    LOOKING = "looking"
    OK = "ok"
    WELL_DONE = "well-done"
    NO = "no"
    ON_MY_WAY = 'on_my_way'

    def __str__(self):
        return self.value


@dataclass_json
@dataclass
class ReactionEntity(Entity):
    type: ReactionType
    creator_id: str
    message_id: str
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())
    creator: UserEntity = field(default_factory=lambda: None)

    def __eq__(self, other):
        return self.uuid == other.uuid
