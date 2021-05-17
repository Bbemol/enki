from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from dataclasses_json import dataclass_json, DataClassJsonMixin
from werkzeug.exceptions import HTTPException

from domain.core.entity import Entity
from domain.users.entities.contact import ContactEntity
from domain.users.entities.group import UserPositionEntity, GroupType


class ThisUserDoesNotFavoriteThisContact(HTTPException):
    code = 404
    description = "Cet utilisateur n'a pas mis ce contact en favoris"


class ThisUserAlreadyFavoriteThisContact(HTTPException):
    code = 409
    description = "Ce contact est déjà en favoris"


@dataclass
class UserEntity(DataClassJsonMixin, Entity):
    """

    """
    first_name: str
    last_name: str
    email: str
    position_id: Optional[str] = field(default_factory=lambda: None)
    group_id: Optional[str] = field(default_factory=lambda: None)
    group_type: GroupType = field(default_factory=lambda: None)
    contacts: List[ContactEntity] = field(default_factory=lambda: [])
    position: Optional[UserPositionEntity] = field(default_factory=lambda: None)
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())
    updated_at: datetime = field(default_factory=lambda: datetime.utcnow())

    def add_contact(self, contact: ContactEntity):
        try:
            _ = self.get_contact(contact=contact)
            raise ThisUserAlreadyFavoriteThisContact()
        except ThisUserDoesNotFavoriteThisContact:
            self.contacts.append(contact)

    def remove_contact(self, contact: ContactEntity):
        _ = self.get_contact(contact=contact)
        self.contacts.remove(contact)

    def get_contacts(self):
        return self.contacts

    def get_contact(self, contact: ContactEntity):
        matches = [c for c in self.contacts if c.uuid == contact.uuid]
        if not matches:
            raise ThisUserDoesNotFavoriteThisContact()
        return matches[0]

    def __repr__(self):
        return f"UserEntity {self.uuid} : {self.first_name}, {self.last_name}"
