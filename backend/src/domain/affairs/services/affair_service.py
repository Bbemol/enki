import xml.dom.minidom
from typing import Any, Dict, List, Union
from uuid import uuid4

from cisu.entities.edxl_entity import EdxlEntity
from requests import Response

from adapters.http.sig import SigApiAdapter
from domain.affairs.entities.affair_entity import AffairEntity
from domain.affairs.entities.simple_affair_entity import SimpleAffairEntity
from domain.affairs.schema.simple_affair import SimpleAffairSchema
from domain.evenements.entities.evenement_entity import EvenementEntity
from domain.evenements.services.message_service import MessageService
from domain.users.entities.user import UserEntity
from service_layer.unit_of_work import AbstractUnitOfWork


class AffairService:
    @staticmethod
    def add_affair(affair: AffairEntity, uow: AbstractUnitOfWork):
        with uow:
            uow.affair.add(affair)
            simple_affair = SimpleAffairEntity(
                uuid=str(uuid4()),
                sge_hub_id=affair.uuid,
                default_affair=affair
            )
            uow.simple_affair.add(simple_affair)
            return affair

    @staticmethod
    def add_affair_from_xml(xml_string: str, uow: AbstractUnitOfWork) -> AffairEntity:
        affair: AffairEntity = AffairService.build_affair_from_xml_string(xml_string=xml_string)
        AffairService.add_affair(affair=affair, uow=uow)
        return affair

    @staticmethod
    def assign_affair_from_evenement(affair_id: str, evenement_id: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            evenement: EvenementEntity = uow.evenement.get_by_uuid(uuid=evenement_id)
            affair: SimpleAffairEntity = uow.simple_affair.get_by_uuid(uuid=affair_id)
            evenement.add_affair(affair=affair)
            MessageService.add_message_from_affair(affair=affair, evenement=evenement, uow=uow)
            return SimpleAffairSchema().dump(affair)

    @staticmethod
    def delete_affair_from_evenement(affair_id: str, evenement_id: str, uow: AbstractUnitOfWork):
        with uow:
            evenement: EvenementEntity = uow.evenement.get_by_uuid(uuid=evenement_id)
            affair: SimpleAffairEntity = uow.simple_affair.get_by_uuid(uuid=affair_id)
            evenement.remove_affair(affair=affair)
            return SimpleAffairSchema().dump(affair)

    @staticmethod
    def get_by_uuid(uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            affair = uow.simple_affair.get_by_uuid(uuid=uuid)
            return SimpleAffairSchema().dump(affair)

    @staticmethod
    def list_affairs(uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            affairs: List[SimpleAffairEntity] = uow.simple_affair.get_all()
            return SimpleAffairSchema(many=True).dump(affairs)

    @staticmethod
    def list_affairs_by_evenement(evenement_id: str, uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            simple_affairs: List[SimpleAffairEntity] = uow.simple_affair.get_by_evenement(uuid=evenement_id)
            return SimpleAffairSchema(many=True).dump(simple_affairs)

    @staticmethod
    def get_user_affairs(user_id: str, uow: AbstractUnitOfWork):
        with uow:
            user: UserEntity = uow.user.get_by_uuid(uuid=user_id)
            affairs: List[SimpleAffairEntity] = uow.simple_affair.match_polygons(
                polygon=user.group.location.polygon
            )
            return SimpleAffairSchema(many=True).dump(affairs)

    @staticmethod
    def list_affairs_by_insee_and_postal_codes(insee_code: Union[str, List[str], None],
                                               postal_code: Union[str, List[str], None],
                                               code_dept: Union[str, List[str], None],
                                               uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            response: Response = SigApiAdapter.code_territory_search(insee_code=insee_code,
                                                                     postal_code=postal_code,
                                                                     code_dept=code_dept)
            result: dict = response.json()
            if result["geometrie"]:
                affairs: List[SimpleAffairEntity] = uow.simple_affair.match_polygons(
                    polygon=result["geometrie"]["coordinates"][0][0])
                return SimpleAffairSchema(many=True).dump(affairs)
            return []

    @staticmethod
    def get_random_affair(uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            affair: AffairEntity = uow.affair.get_one()
            return affair.to_dict()

    @staticmethod
    def get_random_list_affairs(uow: AbstractUnitOfWork, n=10) -> List[Dict[str, Any]]:
        with uow:
            affairs: List[AffairEntity] = uow.affair.get_many(n)
            return [affair.to_dict() for affair in affairs]

    @staticmethod
    def build_affair_from_xml_string(xml_string: str) -> AffairEntity:
        affair_dom = xml.dom.minidom.parseString(xml_string)
        edxl_message = EdxlEntity.from_xml(affair_dom)
        return AffairEntity(**edxl_message.resource.message.choice.to_dict())

    @staticmethod
    def build_affair_from_xml_file(xml_path: str) -> AffairEntity:
        affair_dom = xml.dom.minidom.parse(xml_path)
        edxl_message = EdxlEntity.from_xml(affair_dom)
        return AffairEntity(**edxl_message.resource.message.choice.to_dict())
