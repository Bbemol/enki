from flask import request, current_app, g
from flask_restful import Resource, reqparse
from typing import Union, List

from domain.users.command import CreateUser
from domain.users.services.user_service import UserService
from entrypoints.extensions import event_bus
from entrypoints.middleware import user_info_middleware


class WithUserRepoResource(Resource):
    def __init__(self):
        pass


class UserListResource(WithUserRepoResource):
    """Get all users
    ---
    get:
      parameters:
        - in: query
          required: true
          name: query
          schema:
            type: str
          description: query to find users
      tags:
        - users
      security:
        - jwt: []
      responses:
        200:
          description: Return a list of users
          content:
            application/json:
              schema:
                type: array
                items: UserSchema
    post:
      description: Creating a user
      security:
        - jwt: []
      tags:
        - users
      requestBody:
        content:
          application/json:
            schema:  UserSchema
      responses:
        201:
          description: Successfully created
        400:
          description: bad request, bad parameters
    """

    method_decorators = [user_info_middleware]

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('query', type=str, required=True)
        parser.add_argument('uuids', type=str, required=False, )

        args = parser.parse_args()
        query: str = args.get("query")
        uuids: str = args.get("uuids")
        uuids_list: List[str] = uuids.split(',')
        if isinstance(uuids_list, str):
            uuids_list = [uuids_list]
        users = UserService.search_users(query=query, uuids=uuids_list, uow=current_app.context)

        return {
                   "data": users,
                   "message": "success",
               }, 200

    def post(self):
        body = request.get_json()

        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, required=False)
        args = parser.parse_args()
        body["uuid"] = g.user_info["id"]
        body["email"] = g.user_info["email"]
        body["token"] = args.get("token")
        command = CreateUser(data=body)
        result = event_bus.publish(command, current_app.context)
        return {
                   "message": "success",
                   "data": result[0]
               }, 201


class UserResource(WithUserRepoResource):
    """Get specific user
    ---
    get:
      parameters:
        - in: path
          name: uuid
          schema:
            type: string
          required: true
          description: User id
      tags:
        - users
      responses:
        200:
          description: Return specific user
          content:
            application/json:
              schema: UserSchema
        404:
            description: User not found
    """

    def get(self, uuid: str):
        return {
                   "data": UserService.get_by_uuid(uuid, current_app.context),
                   "message": "success"
               }, 200
