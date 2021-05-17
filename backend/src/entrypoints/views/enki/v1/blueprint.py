from flask import Blueprint, current_app
from flask_restful import Api
from slugify import slugify

from domain.evenements.schemas.message_tag_schema import MessageSchema
from domain.evenements.schemas.evenement_schema import EvenementSchema
from domain.users.schemas.user import UserSchema
from entrypoints.extensions import api_spec
from entrypoints.views.enki.v1.resources.users.user_ressources import UserResource, UserListResource
from .resources import AffairListResource, AffairRandomResource, AffairRandomListResource, \
    MessageListResource, MessageResource, \
    MessageTagResource, MessageTagListResource, \
    TagResource, TagListResource, AffairResource, \
    EvenementListResource, EvenementResource, EvenementClosedResource, \
    ResourceListResource, ResourceResource, \
    MessageResourceResource, MessageResourceListResource, \
    AffairEvenementResource, AffairListEvenementResource
from entrypoints.views.enki.v1.resources.users.contact_ressources import ContactListResource, ContactResource
from entrypoints.views.enki.v1.resources.evenements.envement_invitation_resource import EvenementInviteUserResource
from entrypoints.views.enki.v1.resources.evenements.evenement_resource import MeEvenementResource
from .resources.evenements.evenement_export_resource import EvenementExportResource
from entrypoints.views.enki.v1.resources.users.invitation_ressources import InvitationResource, \
    ValidateInvitationResource
from entrypoints.views.enki.v1.resources.evenements.message_resource_resource import MessageMultipleResourceResource
from .resources.evenements.meeting_ressources import MeetingResource, MeetingListResource, JoinMeetingResource
from .resources.evenements.message_reactions import MessageListReactions
from .resources.users.group_ressources import GroupListResource, GroupTypeListResource, \
    PositionGroupTypeListResource
from .resources.users.location_ressources import LocationListResource, LocationResource
from .resources.users.me.me_affairs_ressources import UserMeAffairsResource
from .resources.users.me.me_ressources import UserMeResource
from .resources.users.user_favorite_ressources import UserContactListResource, UserContactResource

enki_blueprint_v1 = Blueprint(name="enki_blueprint_v1", import_name=__name__, url_prefix="/api/enki/v1")

api = Api(enki_blueprint_v1)

endpoints = {
    # Affairs
    AffairResource: '/affairs/<uuid>',
    AffairListResource: '/affairs',
    AffairRandomResource: '/affair/random',
    AffairRandomListResource: '/affairs/random',
    # Tags
    TagListResource: '/tags',
    TagResource: '/tags/<uuid>',
    MessageTagResource: '/messages/<uuid>/tags/<tag_uuid>',
    MessageTagListResource: '/messages/<uuid>/tags',
    # Resources
    ResourceListResource: '/resources',
    ResourceResource: '/resources/<uuid>',
    # Messages
    MessageResourceResource: '/messages/<uuid>/resource/<resource_uuid>',
    MessageMultipleResourceResource: '/messages/<uuid>/resource/add',
    MessageResourceListResource: '/messages/<uuid>/resources',
    # Evenements
    EvenementListResource: '/events',
    EvenementResource: '/events/<uuid>',
    EvenementClosedResource: '/events/<uuid>/close',
    EvenementInviteUserResource: '/events/<uuid>/invite/<user_uuid>',
    # Evenements <> Messages
    MessageListResource: '/events/<uuid>/messages',
    MessageResource: '/events/<uuid>/messages/<message_uuid>',
    MessageListReactions: '/events/<uuid>/messages/<message_uuid>/react',
    # Evenement <> Affairs
    AffairEvenementResource: '/events/<uuid>/affairs/<affair_uuid>',
    AffairListEvenementResource: '/events/<uuid>/affairs',
    # Evenement <> Export
    EvenementExportResource: '/events/<uuid>/export',
    # Evenement<> Meeting
    MeetingListResource: '/events/<uuid>/meeting',
    MeetingResource: '/events/<uuid>/meeting/<meeting_uuid>',
    JoinMeetingResource: '/events/<uuid>/meeting/<meeting_uuid>/join',
    # User
    UserListResource: '/users',
    UserResource: '/users/<uuid>',
    # Contacts
    ContactListResource: '/contacts',
    ContactResource: '/contacts/<uuid>',
    # Groups
    GroupListResource: '/groups',
    GroupTypeListResource: '/groups/types',
    PositionGroupTypeListResource: '/groups/positions',
    # Location
    LocationListResource: '/locations',
    LocationResource: '/locations/<uuid>',
    # User <> Contacts
    UserContactListResource: '/users/me/contact/favorites',
    UserContactResource: '/users/me/contact/favorites/<contact_uuid>',
    # Me
    UserMeResource: '/users/me',
    UserMeAffairsResource: '/users/me/affairs',
    MeEvenementResource: '/users/me/events',
    # Invitations
    InvitationResource: '/invitation',
    ValidateInvitationResource: '/invitation/validate'
}

inverse_dico = {v:k for k,v in endpoints.items()}

for path, resource  in inverse_dico.items():
    api.add_resource(resource, path, endpoint=slugify(path))


@enki_blueprint_v1.before_app_first_request
def register_views():
    # Add documents Schemas
    api_spec.spec.components.schema("EvenementSchema", schema=EvenementSchema)
    api_spec.spec.components.schema("MessageSchema", schema=MessageSchema)
    api_spec.spec.components.schema("UserSchema", schema=UserSchema)
    # api_spec.spec.components.schema("TagSchema", schema=TagSchema)

    for resource in endpoints:
        api_spec.spec.path(view=resource, app=current_app)
