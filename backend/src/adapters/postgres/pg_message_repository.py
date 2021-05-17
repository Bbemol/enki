from operator import or_
from typing import List

from flask import current_app
from sqlalchemy.orm import Session

from domain.evenements.entities.message_entity import MessageEntity
from domain.evenements.entities.tag_entity import TagEntity
from domain.evenements.ports.message_repository import AbstractMessageRepository, AlreadyExistingMessageUuid, \
    MessagesList
from domain.users.entities.group import GroupEntity
from .repository import PgRepositoryMixin


class PgMessageRepository(PgRepositoryMixin, AbstractMessageRepository):


    def __init__(self, session: Session):
        PgRepositoryMixin.__init__(self, session=session, entity_type=MessageEntity)
        AbstractMessageRepository.__init__(self)

    def _match_uuid(self, uuid: str) -> MessageEntity:
        matches = self.session.query(MessageEntity).filter(MessageEntity.uuid == uuid).all()
        if not matches:
            return None
        return matches[0]

    def _add(self, message: MessageEntity) -> None:
        if self._match_uuid(message.uuid):
            raise AlreadyExistingMessageUuid()
        self.session.add(message)

    def get_all(self) -> List[MessageEntity]:
        return self.session.query(self.entity_type).order_by(self.entity_type.created_at.desc()).all()

    def _match_uuids(self, uuids: List[str]) -> MessagesList:
        matches = self.session.query(self.entity_type).filter(self.entity_type.uuid.in_(uuids)).all()
        return matches

    def get_messages_by_query(self, evenement_id: str, restricted_group_id: str, tag_ids: List[str]) -> MessagesList:
        query = self.session.query(self.entity_type)
        if evenement_id:
            query = query.filter(self.entity_type.evenement_id == evenement_id)

        if restricted_group_id:
            query = query.outerjoin(GroupEntity, MessageEntity.restricted_to).\
                filter(or_(GroupEntity.uuid == restricted_group_id, GroupEntity.uuid==None))
        if tag_ids:
            current_app.logger.info(f"tag_ids {tag_ids}")
            query = query.join(TagEntity, self.entity_type.tags).filter(TagEntity.uuid.in_(tag_ids))

        matches = query.all()
        return matches