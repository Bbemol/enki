from flask import current_app
from flask_restful import Resource, reqparse

from domain.users.entities.group import GroupType
from domain.users.services.group_service import GroupService


class WithGroupRepoResource(Resource):
    def __init__(self):
        pass


class LocationListResource(WithGroupRepoResource):
    """Get all locations
    ---
    get:
      tags:
        - location
      security:
        - jwt: []
      parameters:
        - in: query
          required: true

          name: query
          schema:
            type: str
          description: query to find location
      responses:
        200:
          description: Return a list of groups
          content:
            application/json:
              schema:
                type: array
                items: LocationSchema
    """

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('query', type=str, required=True)

        args = parser.parse_args()
        query: str = args.get("query")

        return {
                   "data": GroupService.list_location_by_query(query=query, uow=current_app.context),
                   "message": "success",
               }, 200


class LocationResource(WithGroupRepoResource):
    """Get specific location
    ---
    get:
      tags:
        - location
      security:
        - jwt: []
      parameters:
        - in: path
          name: uuid
          schema:
            type: string
          required: true
          description: Location id
          description: query to find location
      responses:
        200:
          description: Return specific location
          content:
            application/json:
              schema: LocationSchema
        404:
            description: Contact not found
    """

    def get(self, uuid):
        return {
                   "data": GroupService.get_location_by_uuid(uuid=uuid, uow=current_app.context),
                   "message": "success",
               }, 200
