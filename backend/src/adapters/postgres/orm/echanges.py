from datetime import datetime
from sqlalchemy import Table, Column, String, ForeignKey, Integer, TIMESTAMP, Enum, UniqueConstraint
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import mapper, relationship
from adapters.postgres.orm.metadata import metadata
from domain.echanges.entities.echange_entity import EchangeEntity

echanges_table = Table(
    'echanges', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('payload', TEXT),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now),
)

def start_mappers():
    mapper(EchangeEntity, echanges_table)
