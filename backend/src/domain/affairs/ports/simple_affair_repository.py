import abc
from typing import List, Union
from werkzeug.exceptions import HTTPException

from domain.affairs.entities.simple_affair_entity import SimpleAffairEntity
from domain.evenements.entity import EvenementEntity

simple_affairsList = List[SimpleAffairEntity]


class AlreadyExistingSimpleAffairUuid(HTTPException):
    code = 409
    description = "Cette intervention existe déjà"


class NotFoundSimpleAffair(HTTPException):
    code = 404
    description = "Cette intervention n'existe pas"

class ThisAffairNotAssignToThisEvent(HTTPException):
    code = 404
    description = "Cette intervention n'est pas rataché à cet évenement"


class AbstractSimpleAffairRepository(abc.ABC):
    def add(self, simple_affair: SimpleAffairEntity) -> Union[bool, None]:
        if self._match_uuid(simple_affair.uuid):
            raise AlreadyExistingSimpleAffairUuid()
        result = self._add(simple_affair)
        return result

    def get_one(self) -> SimpleAffairEntity:
        return self.get_all()[0]

    def get_many(self, n: int) -> List[SimpleAffairEntity]:
        return self.get_all()[0:n]

    def get_by_uuid(self, uuid: str) -> SimpleAffairEntity:
        match = self._match_uuid(uuid)
        if not match:
            raise NotFoundSimpleAffair
        return match

    @abc.abstractmethod
    def match_polygons(self, polygon: List) -> List[SimpleAffairEntity]:
        raise NotImplementedError

    def get_by_uuids(self, uuids: List[str]) -> List[SimpleAffairEntity]:
        matches = self._match_uuids(uuids)
        return matches

    def get_by_affair_uuid(self, uuid: str) -> SimpleAffairEntity:
        match = self._match_by_affair_uuid(uuid)
        if not match:
            raise NotFoundSimpleAffair
        return match

    @abc.abstractmethod
    def get_by_evenement(self, uuid: str) -> List[SimpleAffairEntity]:
        raise NotImplementedError

    @abc.abstractmethod
    def _add(self, entity: SimpleAffairEntity):
        raise NotImplementedError

    @abc.abstractmethod
    def _match_uuids(self, uuids: List[str]):
        raise NotImplementedError

    @abc.abstractmethod
    def assign_evenement_to_affair(self, affair: SimpleAffairEntity, evenement: EvenementEntity) -> SimpleAffairEntity:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_affair_from_evenement(self, affair: SimpleAffairEntity) -> SimpleAffairEntity:
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> simple_affairsList:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_uuid(self, uuid: str) -> Union[SimpleAffairEntity, None]:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_by_affair_uuid(self, uuid: str) -> Union[SimpleAffairEntity, None]:
        raise NotImplementedError