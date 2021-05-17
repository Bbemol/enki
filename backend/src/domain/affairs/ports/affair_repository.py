import abc
from typing import List, Union

from flask import current_app
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from werkzeug.exceptions import HTTPException

from domain.affairs.entities.affair_entity import AffairEntity

affairsList = List[AffairEntity]


class AlreadyExistingAffairUuid(HTTPException):
    code = 409
    description = "Cette intervention existe déjà"


class NotFoundAffair(HTTPException):
    code = 404
    description = "Cette intervention n'existe pas"


class AbstractAffairRepository(abc.ABC):
    def add(self, affair: AffairEntity) -> Union[bool, None]:
        if self._match_uuid(affair.uuid):
            raise AlreadyExistingAffairUuid()
        result = self._add(affair)
        return result

    def get_one(self) -> AffairEntity:
        return self.get_all()[0]

    def get_many(self, n: int) -> List[AffairEntity]:
        return self.get_all()[0:n]

    def get_by_uuid(self, uuid: str) -> AffairEntity:
        match = self._match_uuid(uuid)
        if not match:
            raise NotFoundAffair
        return match

    def get_by_uuids(self, uuids: List[str]) -> List[AffairEntity]:
        matches = self._match_uuids(uuids)
        return matches

    @abc.abstractmethod
    def _add(self, entity: AffairEntity):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> affairsList:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_from_polygon(self, multipolygon: List) -> affairsList:
        raise NotImplementedError

    def get_from_polygon(self, multipolygon: List) -> affairsList:
        return self._get_from_polygon(multipolygon)

    @abc.abstractmethod
    def _match_uuid(self, uuid: str) -> Union[AffairEntity, None]:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_uuids(self, uuids: List[str]) -> List[AffairEntity]:
        raise NotImplementedError


class InMemoryAffairRepository(AbstractAffairRepository):
    _affairs: affairsList = []

    def _add(self, entity: AffairEntity):
        self._affairs.append(entity)

    def get_all(self) -> affairsList:
        return self._affairs

    def _match_uuid(self, uuid: str) -> Union[AffairEntity, None]:
        matches = [affair for affair in self._affairs if affair.uuid == uuid]
        if matches:
            return matches[0]

    def _get_from_polygon(self, multipolygon: List) -> affairsList:
        print(len(self.get_all()))
        return [
            affair for affair in self.get_all() if self._contain_point(
                lat=affair.location["lat"],
                lon=affair.location["lon"],
                multipolygon=multipolygon
            )
        ]

    @staticmethod
    def _contain_point(lat: float, lon: float, multipolygon: List) -> bool:
        point = Point(lon, lat)
        polygon = Polygon(multipolygon)
        return polygon.contains(point)

    def _match_uuids(self, uuids: List[str]) -> List[AffairEntity]:
        matches = [affair for affair in self._affairs if affair.uuid in uuids]
        return matches

    # next methods are only for test purposes
    @property
    def affairs(self) -> affairsList:
        return self._affairs

    def set_affairs(self, affairs: affairsList) -> None:
        self._affairs = affairs
