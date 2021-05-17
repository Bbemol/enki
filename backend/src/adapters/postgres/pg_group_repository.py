from typing import List, Union

from flask import current_app
from sqlalchemy.orm import Session
from werkzeug.exceptions import HTTPException

from domain.users.entities.group import GroupEntity, GroupType, PositionGroupTypeEntity, LocationEntity, \
    UserPositionEntity
from domain.users.ports.group_repository import AbstractGroupRepository
from .repository import PgRepositoryMixin

tagsList = List[GroupEntity]


class NotFoundGroup(HTTPException):
    code = 404
    description = "Aucun groupe correspondant à ces critères n'a été trouvé"

class NotFoundLocation(HTTPException):
    code = 404
    description = "Aucune localisation correspondant à ces critères n'a été trouvé"


class NotFoundPosition(HTTPException):
    code = 404
    description = "Cette fonction n'existe pas"

class LocationNotFound(HTTPException):
    code = 404
    description = "Cette localisation n'existe pas"


class PgGroupRepository(PgRepositoryMixin, AbstractGroupRepository):

    def __init__(self, session: Session):
        PgRepositoryMixin.__init__(self, session=session, entity_type=GroupEntity)
        AbstractGroupRepository.__init__(self)

    def _match_uuid(self, uuid: str) -> Union[GroupEntity, None]:
        matches = self.session.query(GroupEntity).filter(GroupEntity.uuid == uuid).all()
        if not matches:
            return None
        return matches[0]

    def get_all(self) -> tagsList:
        return self.session.query(self.entity_type).all()

    def get_position_by_group_type(self, group_type: GroupType) -> List[PositionGroupTypeEntity]:
        matches: List[PositionGroupTypeEntity] = self.session.query(PositionGroupTypeEntity).filter(
            PositionGroupTypeEntity.group_type == group_type).all()
        return matches

    def get_location_by_query(self, query: str, limit=10) -> List[LocationEntity]:
        matches = self.session.query(LocationEntity).filter(
            LocationEntity.search_label.match(query)).limit(limit).all()
        return matches

    def get_location_by_uuid(self, uuid: str) -> LocationEntity:
        matches = self.session.query(LocationEntity).filter(
            LocationEntity.uuid == uuid).all()
        if not matches:
            raise LocationNotFound()
        return matches[0]

    def get_from_group_type_and_location_id(self, group_type: GroupType, location_id: str) -> Union[GroupEntity, None]:
        matches = self.session.query(GroupEntity).filter(GroupEntity.location_id == location_id). \
            filter(GroupEntity.type == group_type).all()
        if not matches:
            raise NotFoundGroup
        return matches[0]

    def get_from_group_type_and_query(self, group_type: GroupType, query: str, limit=10) -> List[GroupEntity]:
        sql_query = self.session.query(GroupEntity).filter(GroupEntity.type == group_type)
        sql_query = sql_query.filter(GroupEntity.label.match(query))
        matches = sql_query.limit(limit).all()
        if not matches:
            raise NotFoundGroup
        return matches

    def add_position(self, position: UserPositionEntity):
        self.session.add(position)

    def get_position(self, position_id: str) -> PositionGroupTypeEntity:
        matches = self.session.query(PositionGroupTypeEntity).filter(PositionGroupTypeEntity.uuid == position_id).all()
        if not matches:
            raise NotFoundPosition
        return matches[0]

    def get_location_by_uuid(self, uuid: str) -> LocationEntity:
        matches = self.session.query(LocationEntity).filter(LocationEntity.uuid == uuid).all()
        if not matches:
            raise NotFoundLocation
        return matches[0]

