from typing import Union, List

from flask import request, current_app, g
from flask_restful import Resource, reqparse

from domain.evenements.commands import CreateMessage
from domain.evenements.entities.evenement_entity import EvenementRoleType
from domain.evenements.entities.reaction_entity import ReactionType
from domain.evenements.services.evenement_service import EvenementService
from domain.evenements.services.message_service import MessageService
from domain.users.services.authorization_service import AuthorizationService
from entrypoints.extensions import event_bus
from entrypoints.middleware import user_info_middleware


class WithMessageRepoResource(Resource):
    def __init__(self):
        pass


class MessageListReactions(WithMessageRepoResource):
    """Get all messages
    ---
    post:
      description: Creating a message
      tags:
        - message
      requestBody:
        content:
          application/json:
            schema:  MessageSchema
      responses:
        201:
          description: Successfully created
          content:
            application/json:
              schema: MessageSchema
        400:
          description: bad request, bad parameters
    """
    method_decorators = [user_info_middleware]

    def get(self, uuid: str, message_uuid: str):
        AuthorizationService.as_access_to_this_evenement_resource(g.user_info["id"], evenement_id=uuid,
                                                                  role_type=EvenementRoleType.VIEW,
                                                                  uow=current_app.context)

        MessageService.get_reactions(message_id=message_uuid,
                                     uow=current_app.context)

    def post(self, uuid: str, message_uuid: str):
        AuthorizationService.as_access_to_this_evenement_resource(g.user_info["id"], evenement_id=uuid,
                                                                  role_type=EvenementRoleType.EDIT,
                                                                  uow=current_app.context)
        body = request.get_json()
        reaction_type = ReactionType[body.get("reaction")]

        creator_id = g.user_info["id"]

        MessageService.add_reaction(creator_id=creator_id,
                                    message_id=message_uuid,
                                    reaction_type=reaction_type,
                                    uow=current_app.context)

        return {
                   "message": "success",
                   "data": "ok"
               }, 201
