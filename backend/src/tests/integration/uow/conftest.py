import pytest
from dotenv import load_dotenv
from sqlalchemy.orm import clear_mappers

from adapters.postgres.base_orm import start_mappers
from entrypoints.config import EnkiConfig
from service_layer.unit_of_work import SqlAlchemyUnitOfWork, AbstractUnitOfWork


@pytest.fixture
def config():
    load_dotenv("/Users/raphael/PycharmProjects/enki/.envs/.test/.env.flaskenv")
    load_dotenv("/Users/raphael/PycharmProjects/enki/.envs/.test/.env.pg")
    config = EnkiConfig()
    return config


@pytest.fixture
def uow(config: EnkiConfig)-> AbstractUnitOfWork:
    clear_mappers()
    start_mappers()
    uow = SqlAlchemyUnitOfWork(config=config)
    return uow