import logging
from datetime import datetime

from geoalchemy2 import Geometry
from sqlalchemy import Table, Column, String, ForeignKey, Integer, TIMESTAMP, Enum, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapper, relationship
from sqlalchemy_utils import ChoiceType

from adapters.postgres.orm.metadata import metadata
from domain.affairs.entities.simple_affair_entity import SimpleAffairEntity
from domain.evenements.entities.evenement_type import EvenementType
from domain.evenements.entities.evenement_entity import EvenementEntity, EvenementRoleType, \
    UserEvenementRole
from domain.evenements.entities.reaction_entity import ReactionType, ReactionEntity
from domain.users.entities.group import LocationEntity
from domain.evenements.entities.message_entity import MessageType, Severity, MessageEntity
from domain.evenements.entities.meeting_entity import MeetingEntity
from domain.evenements.entities.resource import ResourceEntity
from domain.evenements.entities.tag_entity import TagEntity
from domain.users.entities.user import UserEntity
from domain.users.entities.group import GroupEntity

logger = logging.getLogger(__name__)

tagMessageTable = Table(
    'messages_tags', metadata,
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
    Column('external_id', String(60)),
    Column('executor_id', String(60), ForeignKey("users.uuid"), nullable=True),
    Column('creator_id', String(60), ForeignKey("users.uuid")),
    Column('parent_id', String(60), ForeignKey("messages.uuid")),
    Column('done_at', TIMESTAMP()),
    Column('started_at', TIMESTAMP()),
    Column('severity', ChoiceType(Severity, impl=Integer()), nullable=False),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now),
    Column('updated_at', TIMESTAMP(), nullable=False, default=datetime.now, onupdate=datetime.now),
)

message_restricted_table = Table(
    'messages_restricted', metadata,
    Column('messages_uuid', String(60), ForeignKey("messages.uuid")),
    Column('group_uuid', String(60), ForeignKey("groups.uuid")),
)

tagTable = Table(
    'tags', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('title', String(255), nullable=False, unique=True),
    Column('creator_id', String(255), ForeignKey("users.uuid")),
    Column('updated_at', TIMESTAMP(), nullable=False, default=datetime.now, onupdate=datetime.now),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now)
)

user_evenement_role_table = Table(
    'user_evenement_roles', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('user_id', String(255), ForeignKey("users.uuid")),
    Column('evenement_id', String(255), ForeignKey("evenements.uuid")),
    Column('type', ChoiceType(EvenementRoleType, impl=String())),
    Column('revoked_at', TIMESTAMP(), nullable=True),
    Column('updated_at', TIMESTAMP(), nullable=False, default=datetime.now, onupdate=datetime.now),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now)
)


messages_reactions_table = Table(
    'messages_reactions', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('creator_id', String(60), ForeignKey("users.uuid")),
    Column('type', ChoiceType(ReactionType, impl=String())),
    Column('message_id', String(60), ForeignKey("messages.uuid")),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now),
    UniqueConstraint('creator_id', 'type', name='uix_1')

)

resourceTable = Table(
    'resources', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('bucket_name', String(255), nullable=False, unique=False),
    Column('object_path', String(255), nullable=False, unique=False),
    Column('content_type', String(60), nullable=False, unique=False),
    Column('creator_id', String(255), ForeignKey("users.uuid")),
    Column('original_name', String(255)),  # ForeignKey("users.uuid")),
    Column('message_id', String(255), ForeignKey("messages.uuid")),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now)
)

evenementsTable = Table(
    'evenements', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('title', String(255), nullable=False),
    Column('description', String(255)),
    Column('type', Enum(EvenementType)),
    Column('creator_id', String(60), ForeignKey("users.uuid")),
    Column('location_id', String(60), ForeignKey("locations.uuid")),
    Column('started_at', TIMESTAMP(), nullable=False, default=datetime.now),
    Column('ended_at', TIMESTAMP(), nullable=True, default=None),
    Column('updated_at', TIMESTAMP(), nullable=False, default=datetime.now, onupdate=datetime.now),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now)
)

affairsTable = Table(
    'affairs', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('sge_hub_id', String(255), nullable=False),
    Column("location", Geometry('POINT')),
    Column('affair', JSONB()),
    Column('evenement_id', String(60), ForeignKey("evenements.uuid")),
    Column('updated_at', TIMESTAMP(), nullable=False, default=datetime.now, onupdate=datetime.now),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now)
)


meeting_Table = Table(
    'meetings', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('link', String(255), nullable=False),
    Column('creator_id', String(60), ForeignKey("users.uuid")),
    Column('evenement_id', String(60), ForeignKey("evenements.uuid")),
    Column('updated_at', TIMESTAMP(), nullable=False, default=datetime.now, onupdate=datetime.now),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now),
    Column('closed_at', TIMESTAMP(), nullable=True)
)

meeting_participant_table = Table(
    'meeting_participants', metadata,
    Column('meeting_uuid', String(60), ForeignKey("meetings.uuid")),
    Column('user_uuid', String(60), ForeignKey("users.uuid")),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now),
)

def start_mappers():
    mapper(TagEntity, tagTable)
    mapper(EvenementEntity, evenementsTable,
           properties={
               'creator': relationship(UserEntity, backref='evenements', foreign_keys=evenementsTable.c.creator_id,
                                       lazy='noload'),
               'user_roles': relationship(UserEvenementRole, backref='evenements', lazy='noload'),
               'affairs': relationship(SimpleAffairEntity, back_populates='evenement', lazy='noload'),
               'messages': relationship(MessageEntity, backref='evenements', lazy='noload'),
               'location': relationship(LocationEntity, backref='evenements')
           }
           )
    mapper(ResourceEntity, resourceTable)
    mapper(UserEvenementRole, user_evenement_role_table,
           properties={
               'user': relationship(UserEntity, backref='user_evenement_roles'),
           }
           )
    mapper(SimpleAffairEntity, affairsTable,
           properties={
               'evenement': relationship(EvenementEntity, back_populates='affairs', lazy="noload"),
           }
           )
    mapper(MeetingEntity, meeting_Table,
           properties={
               'participants': relationship(UserEntity, lazy="noload",
                                            secondary=meeting_participant_table),
               'creator': relationship(UserEntity, backref='meetings', lazy="noload",
                                       foreign_keys=meeting_Table.c.creator_id, ),
           }
           )
    mapper(
        MessageEntity, messagesTable,
        properties={
            'tags': relationship(TagEntity, backref='messages', secondary=tagMessageTable),
            'resources': relationship(ResourceEntity, backref='messages'),
            'creator': relationship(UserEntity, backref='messages', foreign_keys=messagesTable.c.creator_id),
            'parent': relationship(MessageEntity, uselist=False),
            'reactions': relationship(ReactionEntity, backref='messages'),
            'restricted_to': relationship(GroupEntity, backref='messages', secondary=message_restricted_table)
        }
    )
    mapper(
        ReactionEntity, messages_reactions_table,
        properties={
            'creator': relationship(UserEntity, backref='messages_reactions',uselist=False),
        },
    )