import logging

from datetime import datetime
from sqlalchemy import Table, MetaData, Column, String, ForeignKey, Integer, TIMESTAMP, Enum
from sqlalchemy.orm import mapper, relationship
from sqlalchemy_utils import ChoiceType

from domain.evenements.entity import EvenementType, EvenementEntity
from domain.messages.entities.message_entity import MessageType, Severity, MessageEntity
from domain.messages.entities.tag_entity import TagEntity

logger = logging.getLogger(__name__)

metadata = MetaData()

userTable = Table(
    'users', metadata,
    Column('uuid', String(60), primary_key=True),
)

tagMessageTable = Table(
    'tags_messages', metadata,
    Column('messages_uuid', String(60), ForeignKey("messages.uuid")),
    Column('tag_uuid', String(60), ForeignKey("tags.uuid")),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now),
)


messagesTable = Table(
    'messages', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('title', String(255), nullable=False),
    Column('description', String(255)),
    Column('type', Enum(MessageType)),
    Column('evenement_id', String(60), ForeignKey("evenements.uuid")),
    Column('executor_id', String(60), ForeignKey("users.uuid")),
    Column('creator_id', String(60), ForeignKey("users.uuid")),
    Column('done_at', TIMESTAMP()),
    Column('started_at', TIMESTAMP()),
    Column('severity', ChoiceType(Severity, impl=Integer()), nullable=False),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now),
    Column('updated_at', TIMESTAMP(), nullable=False, default=datetime.now, onupdate=datetime.now),
)
tagTable = Table(
    'tags', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('title', String(255), nullable=False, unique=True),
    Column('creator_id', String(255)),  # ForeignKey("users.uuid")),
    Column('updated_at', TIMESTAMP(), nullable=False, default=datetime.now, onupdate=datetime.now),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now)
)

evenementsTable = Table(
    'evenements', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('title', String(255), nullable=False),
    Column('description', String(255)),
    Column('type', Enum(EvenementType)),
    Column('creator_id', String(255)),  # ForeignKey("users.uuid")),
    Column('started_at', TIMESTAMP(), nullable=False, default=datetime.now),
    Column('ended_at', TIMESTAMP(), nullable=True, default=None),
    Column('updated_at', TIMESTAMP(), nullable=False, default=datetime.now, onupdate=datetime.now),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now)
)

all_tables = [
    userTable,
    tagMessageTable,
    tagTable,
    evenementsTable,
    messagesTable
]


def start_mappers():
    mapper(TagEntity, tagTable)
    mapper(EvenementEntity, evenementsTable)
    mapper(
        MessageEntity, messagesTable,
        properties={
            'tags': relationship(TagEntity, backref='messages', secondary=tagMessageTable)
        }
    )
