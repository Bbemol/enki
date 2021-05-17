import abc

import sqlalchemy as sa
from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_searchable import make_searchable

from adapters.postgres import PgMessageRepository, PgTagRepository, PgEvenementRepository
from adapters.postgres.base_orm import metadata
from adapters.postgres.pg_contact_repository import PgContactRepository
from adapters.postgres.pg_echange_repository import PgEchangeRepository
from adapters.postgres.pg_group_repository import PgGroupRepository
from adapters.postgres.pg_invitation_repository import PgInvitationRepository
from adapters.postgres.pg_meeting_repository import PgMeetingRepository
from adapters.postgres.pg_resource_repository import PgResourceRepository
from adapters.postgres.pg_simple_affair_repository import PgSimpleAffairRepository
from adapters.postgres.pg_user_repository import PgUserRepository
from domain.affairs.ports.affair_repository import AbstractAffairRepository, InMemoryAffairRepository
from domain.affairs.ports.simple_affair_repository import AbstractSimpleAffairRepository
from domain.echanges.ports.echange_repository import AbstractEchangeRepository
from domain.evenements.ports import AbstractTagRepository, AbstractMessageRepository, AbstractResourceRepository
from domain.evenements.ports.evenement_repository import AbstractEvenementRepository, InMemoryEvenementRepository
from domain.evenements.ports.message_repository import InMemoryMessageRepository
from domain.evenements.ports.tag_repository import InMemoryTagRepository
from domain.evenements.ports.meeting_repository import AbstractMeetingRepository
from domain.users.ports.contact_repository import AbstractContactRepository
from domain.users.ports.group_repository import AbstractGroupRepository
from domain.users.ports.invitation_repository import AbstractInvitationRepository
from domain.users.ports.user_repository import AbstractUserRepository
from entrypoints.repositories import ElasticRepositories


class AbstractUnitOfWork(abc.ABC):
    resource: AbstractResourceRepository
    tag: AbstractTagRepository
    message: AbstractMessageRepository
    evenement: AbstractEvenementRepository
    affair: AbstractAffairRepository
    simple_affair: AbstractSimpleAffairRepository
    user: AbstractUserRepository
    contact: AbstractContactRepository
    group: AbstractGroupRepository
    invitation: AbstractInvitationRepository
    meeting: AbstractMeetingRepository
    echange: AbstractEchangeRepository

    def __init__(self, config):
        self.config = config

    def __enter__(self):
        return self

    def __exit__(self, exn_type, exn_value, traceback):
        if exn_type is None:
            self.commit()  # (1)
        else:
            self.rollback()  # (2)

    def init_app(self, app):
        app.context = self

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


def build_engine(sql_engine_uri: str) -> Engine:
    isolation_level = "READ UNCOMMITTED" if "sqlite" in sql_engine_uri else "REPEATABLE READ"
    engine = create_engine(
        sql_engine_uri,
        # isolation_level=isolation_level,
        pool_pre_ping=True
    )
    return engine


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, config):
        super().__init__(config)
        self.engine = build_engine(sql_engine_uri=self.config.DATABASE_URI)
        self.session_factory = sessionmaker(bind=self.engine, autoflush=True)
        sa.orm.configure_mappers()  # IMPORTANT!
        make_searchable(metadata=metadata)

        metadata.create_all(self.engine)

        if config.AFFAIR_REPOSITORY == "ELASTIC":
            self.elastic_repositories = ElasticRepositories(config=self.config)
            self.affair = self.elastic_repositories.affair
        else:
            self.affair = InMemoryAffairRepository()

    def __enter__(self):
        self.session = self.session_factory()
        self.tag = PgTagRepository(self.session)
        self.message = PgMessageRepository(self.session)
        self.evenement = PgEvenementRepository(self.session)
        self.resource = PgResourceRepository(self.session)
        self.simple_affair = PgSimpleAffairRepository(self.session)
        self.user = PgUserRepository(self.session)
        self.contact = PgContactRepository(self.session)
        self.group = PgGroupRepository(self.session)
        self.invitation = PgInvitationRepository(self.session)
        self.meeting = PgMeetingRepository(self.session)
        self.echange = PgEchangeRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        current_app.logger.info("Rollback start")
        self.session.rollback()
