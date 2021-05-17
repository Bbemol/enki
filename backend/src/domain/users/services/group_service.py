from typing import Any, Dict, List

from flask import current_app

from domain.users.entities.group import GroupEntity, GroupType, PositionGroupTypeEntity, LocationEntity
from domain.users.schemas.group import GroupSchema, PositionGroupTypeEntitySchema, LocationSchema, \
    LocationExtendedSchema
from service_layer.unit_of_work import AbstractUnitOfWork


class GroupService:
    schema = GroupSchema

    @staticmethod
    def list_groups(uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            groups: List[GroupEntity] = uow.group.get_all()
            return GroupService.schema(many=True).dump(groups)

    @staticmethod
    def list_group_types(uow: AbstractUnitOfWork) -> List[str]:
        return [e.value for e in list(GroupType)]

    @staticmethod
    def list_positions_by_group_types(group_type: GroupType, uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            positions: List[PositionGroupTypeEntity] = uow.group.get_position_by_group_type(group_type=group_type)
            return PositionGroupTypeEntitySchema(many=True).dump(positions)


    @staticmethod
    def list_groups_from_type_and_query(group_type: GroupType, query: str, uow: AbstractUnitOfWork):
        with uow:
            groups: List[GroupEntity] = uow.group.get_from_group_type_and_query(group_type=group_type, query=query)
            return GroupService.schema(many=True).dump(groups)

    @staticmethod
    def list_location_by_query(query: str, uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            locations: List[LocationEntity] = uow.group.get_location_by_query(query=query)
            return LocationSchema(many=True).dump(locations)

    @staticmethod
    def get_location_by_uuid(uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            location: List[LocationEntity] = uow.group.get_location_by_uuid(uuid=uuid)
            return LocationExtendedSchema().dump(location)
