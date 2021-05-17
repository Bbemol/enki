from flask import request, current_app, g, redirect
from flask_restful import Resource

from domain.evenements.commands import CreateMeeting
from domain.evenements.entities.evenement_entity import EvenementRoleType
from domain.evenements.services.meeting_service import MeetingService
from domain.users.services.authorization_service import AuthorizationService
from entrypoints.extensions import event_bus
from entrypoints.middleware import user_info_middleware


class WithMeetingRepoResource(Resource):
    def __init__(self):
        pass


class MeetingListResource(WithMeetingRepoResource):
    """Get all meetings
    ---
    get:
      tags:
        - meetings
      responses:
        200:
          description: Return a list of meetings
          content:
            application/json:
              schema:
                type: array
                items: MeetingSchema
    post:
      description: Creating a meeting
      tags:
        - meetings
      requestBody:
        content:
          application/json:
            schema:  MeetingSchema
      responses:
        201:
          description: Successfully created
        400:
          description: bad request, bad parameters
    """

    method_decorators = [user_info_middleware]

    def post(self, uuid: str):
        AuthorizationService.as_access_to_this_evenement_resource(g.user_info["id"], evenement_id=uuid,
                                                                  role_type=EvenementRoleType.EDIT,
                                                                  uow=current_app.context)
        body = {
            "creator_id": g.user_info["id"],
            "evenement_id": uuid
        }
        command = CreateMeeting(data=body)
        result = event_bus.publish(command, current_app.context)
        return {
                   "message": "success",
                   "data": result[0]
               }, 201


class MeetingResource(WithMeetingRepoResource):
    """Get specific meeting
    ---
    get:
      parameters:
        - in: path
          name: uuid
          schema:
            type: string
          required: true
          description: Meeting id
      tags:
        - meetings
      responses:
        200:
          description: Return specific meeting
          content:
            application/json:
              schema: MeetingSchema
        404:
            description: Meeting not found
    """

    def get(self, uuid: str, meeting_uuid: str):
        AuthorizationService.as_access_to_this_evenement_resource(g.user_info["id"], evenement_id=uuid,
                                                                  role_type=EvenementRoleType.VIEW, uow=current_app.context)
        return {
                   "data": MeetingService.get_by_uuid(meeting_uuid, current_app.context),
                   "message": "success"
               }, 200


class JoinMeetingResource(WithMeetingRepoResource):
    """Get specific meeting
    ---
    get:
      parameters:
        - in: path
          name: uuid
          schema:
            type: string
          required: true
          description: Meeting id
      tags:
        - meetings
      responses:
        200:
          description: Return specific meeting
          content:
            application/json:
              schema: MeetingSchema
        404:
            description: Meeting not found
    """

    method_decorators = [user_info_middleware]

    def get(self, uuid: str, meeting_uuid: str):
        AuthorizationService.as_access_to_this_evenement_resource(g.user_info["id"], evenement_id=uuid,
                                                                  role_type=EvenementRoleType.VIEW, uow=current_app.context)
        redirect_url = MeetingService.join_meeting(meeting_uuid, user_uuid=g.user_info["id"], uow=current_app.context)
        return {
          "data": {
            "direct_uri": redirect_url
          },
          "message": "success"
        }, 200
