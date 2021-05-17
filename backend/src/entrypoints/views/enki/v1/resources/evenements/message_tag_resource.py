from typing import Dict, Any

from flask_restful import Resource
from flask import current_app, g
from domain.evenements.services.message_service import MessageService


class WithMessageRepoResource(Resource):
    def __init__(self):
        pass


class MessageTagListResource(WithMessageRepoResource):
    """Get message's tags
    ---
    get:
      tags:
        - messages <> tags
      responses:
        200:
          description: Return a list of tags
          content:
            application/json:
              schema:
                type: array
                items: TagSchema

    """

    def get(self, uuid: str):
        tags = MessageService.list_tags(uuid, uow=current_app.context)
        return {"data": tags, "message": "success"}, 200


class MessageTagResource(WithMessageRepoResource):
    """Add, Delete and get specific message's tag
    ---
    get:
      description: Building a relation between a tag and a message
      tags:
        - messages <> tags
      parameters:
        - in: path
          name: uuid
          schema:
            type: string
          required: true
          description: Message id
        - in: path
          name: tag_uuid
          schema:
            type: string
          required: true
          description: Tag id
      responses:
        200:
          description: Return relation

        404:
            description: relation not found
    put:
      description: Building a relation between a tag and a message
      tags:
        - messages <> tags
      parameters:
        - in: path
          name: uuid
          schema:
            type: string
          required: true
          description: Message id
        - in: path
          name: tag_uuid
          schema:
            type: string
          required: true
          description: Tag id
      responses:
        201:
          description: Successfully added relation
        404:
            description: relation not found
    delete:
      description: Deleting a relation between a tag and a message
      tags:
        - messages <> tags
      parameters:
        - in: path
          name: uuid
          schema:
            type: string
          required: true
          description: Message id
        - in: path
          name: tag_uuid
          schema:
            type: string
          required: true
          description: Tag id
      responses:
        202:
          description: Successfully deleted relation
        404:
            description: relation not found
    """

    def get(self, uuid: str, tag_uuid: str):
        tag: Dict[str, Any] = MessageService.get_message_tag(uuid,
                                                             tag_uuid=tag_uuid,
                                                             uow=current_app.context)
        return {"data": tag, "message": "success"}, 200

    def put(self, uuid: str, tag_uuid: str):
        user_uuid=g.user_info["id"]
        MessageService.add_tag_to_message(uuid,
                                          tag_uuid=tag_uuid,
                                          user_uuid=user_uuid,
                                          uow=current_app.context)
        return {"message": f"tag {tag_uuid} successfully added from message {uuid}"}, 201

    def delete(self, uuid: str, tag_uuid: str):
        user_uuid = g.user_info["id"]
        MessageService.remove_tag_to_message(uuid,
                                             tag_uuid=tag_uuid,
                                             user_uuid=user_uuid,
                                             uow=current_app.context)
        return {"message": f"tag {tag_uuid} successfully deleted from message {uuid}"}, 202
