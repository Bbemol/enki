from flask import request, current_app, g
from flask_restful import Resource

from domain.evenements.commands import CreateResource
from domain.evenements.services.resource_service import ResourceService
from entrypoints.extensions import event_bus
from entrypoints.middleware import user_info_middleware


class WithResourceRepoResource(Resource):
    def __init__(self):
        pass


class ResourceListResource(WithResourceRepoResource):
    """Get all resources
    ---
    post:
      description: Creating a resource
      tags:
        - resources
      requestBody:
        content:
          application/json:
            schema:  ResourceSchema
      responses:
        201:
          description: Successfully created
        400:
          description: bad request, bad parameters

    """
    method_decorators = [user_info_middleware]

    def post(self):
        body = request.get_json()
        body["creator_id"] = g.user_info["id"]
        create_command = CreateResource(data=body)
        result = event_bus.publish(create_command, current_app.context)
        return {"message": "success",
                "data": result[0]}, 201


class ResourceResource(WithResourceRepoResource):
    """Get specific resource
    ---
    get:
      tags:
        - resources
      parameters:
        - in: path
          name: uuid
          schema:
            type: string
          required: true
          description: Tag id
      responses:
        200:
          description: Return specific resource
          content:
            application/json:
              schema: ResourceSchema
        404:
            description: Resource not found
    delete:
      tags:
        - resources
      parameters:
        - in: path
          name: uuid
          schema:
            type: string
          required: true
          description: Tag id
      responses:
        200:
          description: Successfully deleted
        404:
            description: Resource not found
    """
    method_decorators = [user_info_middleware]

    def get(self, uuid: str):
        return {
                   "data": ResourceService.get_resource(uuid=uuid, uow=current_app.context),
                   "message": "success"
               }, 200

    def delete(self, uuid: str):
        user_uuid = g.user_info["id"]
        ResourceService.delete_resource(uuid=uuid, user_uuid=user_uuid, uow=current_app.context),
        return {
                   "message": "success"
               }, 200
