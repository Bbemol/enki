import abc
from typing import List, Union

from flask import current_app
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from werkzeug.exceptions import HTTPException

from domain.echanges.entities.echange_entity import EchangeEntity
from domain.echanges.entities.echange_entity import EchangeEntity

echangesList = List[EchangeEntity]


class AlreadyExistingEchangeUuid(HTTPException):
    code = 409
    description = "Cet échange existe déjà"


class NotFoundEchange(HTTPException):
    code = 404
    description = "Cet échange n'existe pas"


class AbstractEchangeRepository(abc.ABC):
    def add(self, echange: EchangeEntity) -> Union[bool, None]:
        result = self._add(echange)
        return result

    def get_by_uuid(self, uuid: str) -> EchangeEntity:
        match = self._match_uuid(uuid)
        if not match:
            raise NotFoundEchange
        return match

    @abc.abstractmethod
    def _match_uuid(self, uuid: str) -> Union[EchangeEntity, None]:
        raise NotImplementedError

    @abc.abstractmethod
    def _add(self, entity: EchangeEntity):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> echangesList:
        raise NotImplementedError


class InMemoryEchangeRepository(AbstractEchangeRepository):
    _echanges: echangesList = []

    def _add(self, entity: EchangeEntity):
        self._echanges.append(entity)

    def get_all(self) -> echangesList:
        return self._echanges