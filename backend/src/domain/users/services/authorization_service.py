from enum import Enum, auto
from typing import Any, Dict, List

from flask import current_app
from werkzeug.exceptions import HTTPException

from domain.evenements.entities.evenement_entity import EvenementRoleType
from service_layer.unit_of_work import AbstractUnitOfWork


class EvenementActionForbiddenException(HTTPException):
    code = 401
    description = "Action interdite sur cet évenement"

class AuthorizationService:
    @staticmethod
    def as_access_to_this_evenement_resource(user_id: str, evenement_id: str,  role_type: EvenementRoleType, uow: AbstractUnitOfWork) -> bool:
        with uow:
            evenement = uow.evenement.get_by_uuid(uuid=evenement_id)
            if evenement.creator_id == user_id or evenement.user_has_access(user_id=user_id, role_type=role_type):
                return True
            else:
                raise EvenementActionForbiddenException()


