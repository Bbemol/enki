from typing import Any, Dict, List, Optional
from uuid import uuid4

from flask import current_app
from marshmallow import ValidationError

from adapters.http.keycloak import KeycloakHelper
from domain.affairs.entities.simple_affair_entity import SimpleAffairEntity
from domain.affairs.schema.simple_affair import SimpleAffairSchema
from domain.users.entities.contact import ContactEntity
from domain.users.entities.group import UserPositionEntity, PositionGroupTypeEntity, GroupTypeNotMatchException
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
        token: str = data.pop("token", None)
        try:
            user: UserEntity = UserService.schema().load(data)
        except ValidationError as ve:
            raise ve

        with uow:
            _ = uow.user.add(user)

            user_position = UserService.build_position_from_group_id_ad_position_id(
                group_id=user.group_id,
                position_id=user.position_id,
                group_type=user.group_type,
                uow=uow
            )
            user.position = user_position

            UserService.handle_keycloak(
                uuid=user.uuid,
                first_name=user.first_name,
                last_name=user.last_name,
                group_type=user.group_type,
                fonction=user.position.position.slug
            )

            uuid = str(user.uuid)

        return UserService.get_by_uuid(uuid=uuid, uow=uow)

    @staticmethod
    def handle_keycloak(uuid: str, first_name: str, last_name: str,
                        fonction: str, group_type: str):
        kh = KeycloakHelper.from_config(EnkiConfig())

        kh.update_user_at_creation(
            user_id=uuid,
            first_name=first_name,
            last_name=last_name,
            attributes={
                "fonction": fonction,
                "group_type": group_type,
            }
        )
        kh.assign_to_group(user_id=uuid, group_name=group_type.replace("é", "e").lower())

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
    def search_users(query: str, uow: AbstractUnitOfWork, uuids: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        with uow:
            users: List[UserEntity] = uow.user.search(query=query, uuids=uuids)
            return UserService.schema(many=True).dump(users)

    @staticmethod
    def list_contacts(uuid: str, uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            user: UserEntity = uow.user.get_by_uuid(uuid=uuid)
            contacts: List[ContactEntity] = user.get_contacts()
            return ContactSchema(many=True).dump(contacts)

    @staticmethod
    def get_user_contact(uuid: str, contact_uuid: str, uow: AbstractUnitOfWork):
        with uow:
            user: UserEntity = uow.user.get_by_uuid(uuid=uuid)
            contact = uow.contact.get_by_uuid(uuid=contact_uuid)
            user.get_contact(contact=contact)
            return ContactSchema(many=True).dump(contact)

    @staticmethod
    def add_contact_to_user(uuid: str, contact_uuid: str, uow: AbstractUnitOfWork):
        with uow:
            user: UserEntity = uow.user.get_by_uuid(uuid=uuid)

            contact = uow.contact.get_by_uuid(uuid=contact_uuid)
            user.add_contact(contact=contact)
            return ContactSchema().dump(contact)

    @staticmethod
    def remove_contact_to_user(uuid: str, contact_uuid: str, uow: AbstractUnitOfWork):
        with uow:
            user: UserEntity = uow.user.get_by_uuid(uuid=uuid)
            contact = uow.contact.get_by_uuid(uuid=contact_uuid)
            user.remove_contact(contact=contact)
            return ContactSchema().dump(contact)

    @staticmethod
    def get_affairs_by_user_uuid(uuid: str, uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            user: UserEntity = uow.user.get_by_uuid(uuid=uuid)
            affairs: List[SimpleAffairEntity] = uow.simple_affair.match_polygons(
                polygon=user.position.group.location.polygon
            )
            return SimpleAffairSchema(many=True).dump(affairs)

    @staticmethod
    def build_position_from_group_id_ad_position_id(
            group_id: str, position_id: str, group_type: str, uow: AbstractUnitOfWork
    ):
        group = uow.group.get_by_uuid(uuid=group_id)
        if group.type != group_type:
            raise GroupTypeNotMatchException()

        position: PositionGroupTypeEntity = uow.group.get_position(position_id=position_id)
        if position.group_type != group_type:
            raise GroupTypeNotMatchException()

        user_position = UserPositionEntity(uuid=str(uuid4()))
        user_position.group = group
        user_position.position = position
        uow.group.add_position(user_position)
        return user_position
