from dataclasses import fields
from datetime import datetime
from typing import Any, Dict, List, Union
from uuid import uuid4
import pandas as pd
from flask import current_app
from marshmallow import ValidationError

from domain.affairs.entities.simple_affair_entity import SimpleAffairEntity
from domain.affairs.schema.simple_affair import SimpleAffairSchema
from domain.core.events import UserEventInvitationCreated
from domain.evenements.entities.evenement_entity import EvenementEntity, EvenementRoleType, UserEvenementRole
from domain.evenements.entities.message_entity import MessageEntity
from domain.evenements.schemas.message_tag_schema import MessageSchema
from domain.evenements.schemas.evenement_schema import EvenementSchema
from domain.evenements.services.message_service import MessageService
from domain.users.entities.group import LocationEntity
from domain.users.entities.user import UserEntity
from domain.users.schemas.user import UserSchema
from entrypoints.extensions import event_bus
from service_layer.unit_of_work import AbstractUnitOfWork


class EvenementService:
    schema = EvenementSchema

    @staticmethod
    def add_evenement(data: dict,
                      uow: AbstractUnitOfWork):
        creator_id = data.pop("creator_id")
        try:
            evenement: EvenementEntity = EvenementService.schema().load(data)

        except ValidationError as ve:
            raise ve

        with uow:

            user: UserEntity = uow.user.get_by_uuid(uuid=creator_id)
            user_event_role: UserEvenementRole = UserEvenementRole(
                uuid=str(uuid4()),
                user_id=user.uuid,
                evenement_id=evenement.uuid,
                type=EvenementRoleType.CREATOR
            )
            if evenement.uuid:
                location: LocationEntity = uow.group.get_location_by_uuid(evenement.location_id)
            _ = uow.evenement.add(evenement)
            evenement.set_location(location)
            evenement.creator = user

            user_event_role.user = user
            evenement.add_user_role(user_role=user_event_role)
            evenement_uuid = str(evenement.uuid)

        final_evenement: EvenementEntity = uow.evenement.get_by_uuid(uuid=evenement_uuid)
        return EvenementService.schema().dump(final_evenement)

    @staticmethod
    def get_by_uuid(uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            return EvenementService.schema().dump(uow.evenement.get_by_uuid(uuid=uuid))

    @staticmethod
    def invite_user(uuid: str, user_id: str, role_type: EvenementRoleType, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            evenement: EvenementEntity = uow.evenement.get_by_uuid(uuid=uuid)
            user: UserEntity = uow.user.get_by_uuid(uuid=user_id)
            user_event_role: UserEvenementRole = UserEvenementRole(
                uuid=str(uuid4()),
                user_id=user.uuid,
                evenement_id=evenement.uuid,
                type=role_type
            )
            user_event_role.user = user
            evenement.add_user_role(user_role=user_event_role)
            event_bus.publish(UserEventInvitationCreated(data={
                "email": user.email,
                "evenement_id": evenement.uuid,
                "evenement_title": evenement.title
            }))
            return UserSchema().dump(uow.user.get_by_uuid(uuid=user_id))

    @staticmethod
    def change_user_role(uuid: str, user_id: str, role_type: EvenementRoleType, uow: AbstractUnitOfWork) -> Dict[
        str, Any]:
        with uow:
            evenement: EvenementEntity = uow.evenement.get_by_uuid(uuid=uuid)
            user: UserEntity = uow.user.get_by_uuid(uuid=user_id)
            evenement.change_access_type(user_id=user_id, role_type=role_type)
            return UserSchema().dump(user)

    @staticmethod
    def get_evenements_by_user_id(user_uuid: str, uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            evenements: List[EvenementEntity] = uow.evenement.list_from_user_id(user_uuid=user_uuid)
            return EvenementService.schema(many=True).dump(evenements)

    @staticmethod
    def revoke_access(uuid: str, user_id: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            evenement: EvenementEntity = uow.evenement.get_by_uuid(uuid=uuid)
            user: UserEntity = uow.user.get_by_uuid(uuid=user_id)
            evenement.revoke_user_access(user_id=user_id)
            return UserSchema().dump(user)

    @staticmethod
    def list_evenements(uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            evenements: List[EvenementEntity] = uow.evenement.get_all()
            return EvenementService.schema(many=True).dump(evenements)

    @staticmethod
    def list_affairs_by_evenement(evenement_id: str, uow: AbstractUnitOfWork) -> List[SimpleAffairEntity]:
        with uow:
            simple_affairs: List[SimpleAffairEntity] = uow.simple_affair.get_by_evenement(uuid=evenement_id)
            return simple_affairs

    @staticmethod
    def finish_evenement(uuid: str, uow: AbstractUnitOfWork):
        with uow:
            evenement: EvenementEntity = uow.evenement.get_by_uuid(uuid=uuid)
            evenement.ended_at = datetime.now()
            return EvenementService.schema().dump(evenement)

    @staticmethod
    def list_affairs(uuid: str, uow: AbstractUnitOfWork):
        with uow:
            evenement: EvenementEntity = uow.evenement.get_by_uuid(uuid=uuid)
            return SimpleAffairSchema(many=True).dump(evenement.get_affairs())

    @staticmethod
    def get_message_by_uuid(uuid: str, message_uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            _ = uow.evenement.get_by_uuid(uuid=uuid)
            message = uow.message.get_by_uuid(uuid=message_uuid)
            return MessageSchema().dump(message)

    @staticmethod
    def list_messages(uuid: str, uow: AbstractUnitOfWork):
        with uow:
            evenement: EvenementEntity = uow.evenement.get_by_uuid(uuid=uuid)
            to_return = []
            for message in evenement.get_messages():

                    to_return.append(MessageSchema().dump(message))


            return to_return

    @staticmethod
    def list_messages_by_query(uuid: str,
                               creator_id: str,
                               tag_ids: Union[str, List[str], None],
                               uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        if isinstance(tag_ids, str):
            tag_ids = [tag_ids]


        with uow:
            user = uow.user.get_by_uuid(uuid=creator_id)
            _ = uow.evenement.get_by_uuid(uuid=uuid)
            messages: List[MessageEntity] = uow.message.get_messages_by_query(
                evenement_id=uuid,
                restricted_group_id=user.position.group_id,
                tag_ids=tag_ids)
            return MessageService.schema(many=True).dump(messages)

    @staticmethod
    def create_list_of_dict_entries(uuid: str, uow: AbstractUnitOfWork) -> List[Dict]:
        data_dict = []
        with uow:
            evenement: EvenementEntity = uow.evenement.get_by_uuid(uuid=uuid)
            for message in evenement.get_all_entries():
                data_dict.append(MessageSchema().dump(message))
        return data_dict

    @staticmethod
    def create_dataframe(uuid: str, uow: AbstractUnitOfWork) -> pd.DataFrame:
        entries = EvenementService.create_list_of_dict_entries(uuid=uuid, uow=uow)
        df = pd.DataFrame(entries).sort_values("created_at", ascending=False)
        return df
