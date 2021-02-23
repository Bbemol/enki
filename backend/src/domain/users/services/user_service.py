from typing import Any, Dict, List
from uuid import uuid4

from flask import current_app
from marshmallow import ValidationError

from adapters.http.keycloak import KeycloakHelper
from domain.affairs.entities.simple_affair_entity import SimpleAffairEntity
from domain.affairs.schema.simple_affair import SimpleAffairSchema
from domain.affairs.services.affair_service import AffairService
from domain.users.entities.group import GroupType, UserPositionEntity
from domain.users.entities.user import UserEntity
from domain.users.schemas.contact import ContactSchema
from domain.users.schemas.user import UserSchema
from entrypoints.config import EnkiConfig
from service_layer.unit_of_work import AbstractUnitOfWork


class UserService:
    schema = UserSchema

    @staticmethod
    def add_user(data: dict,
                 uow: AbstractUnitOfWork):

        position_id = data.pop("position_id", None)
        location_id = data.pop("location_id", None)
        group_type = data.pop("group_type", None)

        try:
            user: UserEntity = UserService.schema().load(data)
            return_value = UserService.schema().dump(user)
            current_app.logger.info(f"return_value {return_value}")

        except ValidationError as ve:
            raise ve

        with uow:
            kh = KeycloakHelper.from_config(EnkiConfig())
            _ = uow.user.add(user)
            group = uow.group.get_from_group_type_and_location_id(group_type=group_type, location_id=location_id)

            position = uow.group.get_position(position_id=position_id)
            user_position = UserPositionEntity(uuid=str(uuid4()))
            user_position.group = group
            user_position.position = position
            uow.group.add_position(user_position)
            user.position = user_position

            kh.update_user_at_creation(
                user_id=user.uuid,
                first_name=user.first_name,
                last_name=user.last_name,
                attributes={
                    "fonction": user.position.position.slug,
                    "group_type": group_type,
                }
            )
            current_app.logger.info(f"after updating in keycloak {str(user.position.position.slug).lower()}")
            kh.assign_to_group(user_id=user.uuid, group_name=str(user.position.position.slug).lower())

        return return_value

    @staticmethod
    def get_by_uuid(uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            return UserService.schema().dump(uow.user.get_by_uuid(uuid=uuid))

    @staticmethod
    def list_users(uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            users: List[UserEntity] = uow.user.get_all()
            return UserService.schema(many=True).dump(users)

    @staticmethod
    def list_contacts(uuid: str, uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            contacts: List[UserEntity] = uow.user.get_user_contacts(uuid=uuid)
            return ContactSchema(many=True).dump(contacts)

    @staticmethod
    def get_user_contact(uuid: str, contact_uuid: str, uow: AbstractUnitOfWork):
        with uow:
            contact = uow.contact.get_by_uuid(uuid=contact_uuid)
            uow.user.get_user_contact(uuid=uuid, contact=contact)
            return ContactSchema(many=True).dump(contact)


    @staticmethod
    def add_contact_to_user(uuid: str, contact_uuid: str, uow: AbstractUnitOfWork):
        with uow:
            contact = uow.contact.get_by_uuid(uuid=contact_uuid)
            uow.user.add_user_contact(uuid=uuid, contact=contact)
            return ContactSchema().dump(contact)


    @staticmethod
    def remove_contact_to_user(uuid: str, contact_uuid: str, uow: AbstractUnitOfWork):
        with uow:
            contact = uow.contact.get_by_uuid(uuid=contact_uuid)
            uow.user.remove_user_contact(uuid=uuid, contact=contact)
            return ContactSchema().dump(contact)

    @staticmethod
    def get_affairs_by_user_uuid(uuid: str, uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            user: UserEntity = uow.user.get_by_uuid(uuid=uuid)
            affairs: List[SimpleAffairEntity] = uow.simple_affair.match_polygons(
                polygon=user.position.group.location.polygon
            )
            return SimpleAffairSchema(many=True).dump(affairs)

