from typing import List, Union

from sqlalchemy.orm import Session

from domain.echanges.entities.echange_entity import EchangeEntity
from domain.echanges.ports.echange_repository import AbstractEchangeRepository, AlreadyExistingEchangeUuid
from .repository import PgRepositoryMixin

echangesList = List[EchangeEntity]


class PgEchangeRepository(PgRepositoryMixin, AbstractEchangeRepository):
    def __init__(self, session: Session):
        PgRepositoryMixin.__init__(self, session=session, entity_type=EchangeEntity)
        AbstractEchangeRepository.__init__(self)

    def _match_uuid(self, uuid: str) -> Union[EchangeEntity, None]:
        matches = self.session.query(EchangeEntity).filter(EchangeEntity.uuid == uuid).all()
        if not matches:
            return None
        return matches[0]

    def _add(self, echange: EchangeEntity):
        if self._match_uuid(echange.uuid):
            raise AlreadyExistingEchangeUuid()
        self.session.add(echange)

    def get_all(self) -> echangesList:
        return self.session.query(self.entity_type).all()