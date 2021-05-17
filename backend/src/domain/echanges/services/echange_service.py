from domain.echanges.entities.echange_entity import EchangeEntity
from service_layer.unit_of_work import AbstractUnitOfWork


class EchangeService:
    @staticmethod
    def add_echange(echange: EchangeEntity, uow: AbstractUnitOfWork):
        with uow:
            uow.echange.add(echange)

