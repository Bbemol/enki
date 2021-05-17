from flask import current_app, g
from flask_restful import Resource, reqparse

from domain.evenements.entities.evenement_entity import EvenementRoleType
from domain.evenements.services.evenement_service import EvenementService
from domain.users.services.authorization_service import AuthorizationService
from entrypoints.middleware import user_info_middleware


class WithEvenementRepoResource(Resource):
    def __init__(self):
        pass


class EvenementInviteUserResource(WithEvenementRepoResource):
    """Invite user on an event
    ---
    put:
      description: Creating an event
      tags:
        - events
      parameters:
        - in: query
          name: role_type
          required: false
          enum:
            - view
            - edit
            - admin
          schema:
            type: str
          description: Role type
        - in: path
          name: uuid
          schema:
            type: string
          required: true
          description: Event id
        - in: path
          name: user_uuid
          schema:
            type: string
          required: true
          description: User uuid
      responses:
        201:
          description: Successfully added
          content:
            application/json:
              schema:
                type: array
                items: UserSchema
        400:
          description: bad request, bad parameters
        409:
          description: User already has access
    delete:
      description: revoke access to an event
      tags:
        - events
      parameters:
        - in: path
          name: uuid
          schema:
            type: string
          required: true
          description: Event id
        - in: path
          name: user_uuid
          schema:
            type: string
          required: true
          description: User uuid
      responses:
        202:
          description: Successfully created
          content:
            application/json:
              schema:
                type: array
                items: UserSchema
        400:
          description: bad request, bad parameters
    """
    method_decorators = [user_info_middleware]

    def put(self, uuid: str, user_uuid: str):
        AuthorizationService.as_access_to_this_evenement_resource(g.user_info["id"],
                                                                  evenement_id=uuid,
                                                                  role_type=EvenementRoleType.ADMIN,
                                                                  uow=current_app.context)
        parser = reqparse.RequestParser()
        parser.add_argument('role_type', type=str, required=False,     choices=([e.value for e in EvenementRoleType]))

        args = parser.parse_args()
        role_type: EvenementRoleType = args.get("role_type")
        if role_type:
            result = EvenementService.change_user_role(uuid=uuid, user_id=user_uuid,
                                                       role_type=role_type,
                                                       uow=current_app.context)
        else:
            result = EvenementService.invite_user(uuid=uuid,
                                                  user_id=user_uuid,
                                                  role_type=EvenementRoleType.VIEW,
                                                  uow=current_app.context)
        return {
                   "message": "success",
                   "data": result,
               }, 201

    def delete(self, uuid: str, user_uuid: str):
        AuthorizationService.as_access_to_this_evenement_resource(g.user_info["id"], evenement_id=uuid,
                                                                  role_type=EvenementRoleType.ADMIN, uow=current_app.context)
        result = EvenementService.revoke_access(uuid=uuid,
                                                user_id=user_uuid,
                                                uow=current_app.context)
        return {
                   "message": "success",
                   "data": result,
               }, 202
