from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Union, Optional, List

from dataclasses_json import dataclass_json
from werkzeug.exceptions import HTTPException

from domain.affairs.entities.simple_affair_entity import SimpleAffairEntity
from domain.core.entity import Entity
from domain.evenements.entities.message_entity import MessageEntity
from domain.users.entities.group import LocationEntity
from domain.users.entities.user import UserEntity
from domain.evenements.entities.evenement_type import EvenementType


class EvenementClosedException(HTTPException):
    code = 410
    description = "Evenement is closed"


class UserAlreadyAccessEvenement(HTTPException):
    code = 409
    description = "Cet utilisateur à déjà accès à cet évenement"


class UserHasNoAccessEvenement(HTTPException):
    code = 409
    description = "Cet utilisateur n'à pas accès à cet évenement"


class EvenementRoleType(str, Enum):
    CREATOR = "creator"
    ADMIN = "admin"
    EDIT = "edit"
    VIEW = "view"


evenement_role_dependancies = {
    EvenementRoleType.CREATOR: [EvenementRoleType.ADMIN, EvenementRoleType.EDIT, EvenementRoleType.VIEW],
    EvenementRoleType.ADMIN: [EvenementRoleType.EDIT, EvenementRoleType.VIEW],
    EvenementRoleType.EDIT: [EvenementRoleType.VIEW],
    EvenementRoleType.VIEW: [],
}


@dataclass_json
@dataclass
class UserEvenementRole(Entity):
    user_id: str
    evenement_id: str
    type: EvenementRoleType
    user: UserEntity = field(default_factory=lambda: None)
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())
    revoked_at: Optional[datetime] = field(default_factory=lambda: None)
    updated_at: datetime = field(default_factory=lambda: datetime.utcnow())

    def is_active(self):
        return self.revoked_at is None or self.revoked_at > datetime.now()

    def revoke(self):
        self.revoked_at = datetime.now()


@dataclass_json
@dataclass
class EvenementEntity(Entity):
    """

    """
    title: str
    description: Union[str, None]
    type: EvenementType
    started_at: datetime
    location_id: Optional[str] = field(default_factory=lambda: None)
    location: Optional[LocationEntity] = field(default_factory=lambda: None)
    creator_id: Optional[str] = field(default_factory=lambda: None)
    creator: Optional[UserEntity] = field(default_factory=lambda: None)
    messages: List[MessageEntity] = field(default_factory=lambda: [])
    affairs: List[SimpleAffairEntity] = field(default_factory=lambda: [])
    user_roles: List[UserEvenementRole] = field(default_factory=lambda: [])
    ended_at: Union[datetime, None] = field(default_factory=lambda: None)
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())
    updated_at: datetime = field(default_factory=lambda: datetime.utcnow())

    @property
    def closed(self) -> bool:
        return self.ended_at and self.ended_at < datetime.now()

    def close(self):
        self.ended_at = datetime.now()

    def check_can_assign(self) -> bool:
        if self.closed:
            raise EvenementClosedException
        return True

    def add_message(self, message: MessageEntity):
        self.messages.append(message)

    def add_affair(self, affair: SimpleAffairEntity):
        self.affairs.append(affair)

    def remove_affair(self, affair: SimpleAffairEntity):
        self.affairs.remove(affair)

    def change_access_type(self, user_id: str, role_type: EvenementRoleType) -> UserEvenementRole:
        for role in self.user_roles:
            if role.user_id == user_id:
                role.type = role_type
                return role
        raise UserHasNoAccessEvenement()

    def add_user_role(self, user_role: UserEvenementRole) -> UserEvenementRole:
        for role in self.user_roles:
            if role.user_id == user_role.user_id and user_role.uuid != role.uuid:
                raise UserAlreadyAccessEvenement()
        self.user_roles.append(user_role)
        return user_role

    def revoke_user_access(self, user_id) -> UserEvenementRole:
        for user_role in self.user_roles:
            if user_role.user_id == user_id:
                user_role.revoke()
                return user_role
        raise UserHasNoAccessEvenement()

    def user_has_access(self, user_id: str, role_type: EvenementRoleType = EvenementRoleType.VIEW) -> bool:
        for user_role in self.user_roles:
            if user_role.user_id == user_id and user_role.is_active() \
                    and (
                    user_role.type == role_type or role_type in evenement_role_dependancies.get(user_role.type, [])):
                return True
        return False

    def get_affairs(self) -> List[SimpleAffairEntity]:
        return self.affairs

    def get_messages(self) -> List[MessageEntity]:
        return self.messages

    def get_all_entries(self) -> List[MessageEntity]:
        entries: List[MessageEntity] = self.messages + \
            [MessageEntity.from_affair(affair=affair) for affair in self.affairs]
        return entries

    def set_location(self, location: LocationEntity):
        self.location_id = location.uuid
        self.location = location



