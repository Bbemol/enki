from typing import List, Union

from sqlalchemy import or_
from sqlalchemy.orm import Session, lazyload, subqueryload, contains_eager
from domain.evenements.entities.evenement_type import EvenementType

from domain.evenements.entities.evenement_entity import EvenementEntity, UserEvenementRole
from domain.evenements.ports.evenement_repository import AbstractEvenementRepository, AlreadyExistingEvenementUuid
from .repository import PgRepositoryMixin


class PgEvenementRepository(PgRepositoryMixin, AbstractEvenementRepository):

    def __init__(self, session: Session):
        PgRepositoryMixin.__init__(self, session=session, entity_type=EvenementEntity)

    def _match_uuid(self, uuid: str, load_query=None) -> Union[EvenementEntity, None]:
        query = self.session.query(EvenementEntity).filter(EvenementEntity.uuid == uuid).options(lazyload("*"))
        matches = query.all()

        if matches:
            return matches[0]

    def _add(self, evenement: EvenementEntity) -> None:
        if self._match_uuid(evenement.uuid):
            raise AlreadyExistingEvenementUuid()
        self.session.add(evenement)

    def get_all(self) -> List[EvenementEntity]:
        return self.session.query(self.entity_type).options(lazyload('*')).all()

    def list_from_user_id(self, user_uuid: str) -> List[EvenementEntity]:
        return self.session.query(self.entity_type).outerjoin(UserEvenementRole).options(lazyload('*')).filter(
            or_(
                EvenementEntity.creator_id == user_uuid,
                UserEvenementRole.user_id == user_uuid
            )
        ).all()
