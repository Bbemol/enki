from typing import Any, Dict, List
from marshmallow import ValidationError

from adapters.http.keycloak import KeycloakHelper
from domain.users.entities.user import UserEntity
from domain.users.schemas.user import UserSchema
from entrypoints.config import EnkiConfig
from service_layer.unit_of_work import AbstractUnitOfWork


class UserService:
    schema = UserSchema

    @staticmethod
    def add_user(data: dict,
                 uow: AbstractUnitOfWork):

        code_insee = data.pop("code_insee")
        try:
            user: UserEntity = UserService.schema().load(data)
            return_value = UserService.schema().dump(user)
        except ValidationError as ve:
            raise ve

        with uow:
            kh = KeycloakHelper.from_config(EnkiConfig())
            _ = uow.user.add(user)
            kh.update_user_at_creation(
                user_id=user.uuid,
                first_name=user.first_name,
                last_name=user.last_name,
                attributes={
                    "fonction": user.position,
                    "code_insee": code_insee,
                }
            )
            kh.assign_to_group(user_id=user.uuid, group_name=str(user.position).lower())

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
