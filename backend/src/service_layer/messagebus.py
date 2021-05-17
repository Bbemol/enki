from typing import List, Dict, Callable, Type

from domain.core import topics
from domain.core.topics import Topic
from .handlers import events, commands

EVENT_HANDLERS: Dict[Type[Topic], List[Callable]] = {
    #topics.AffairCreatedTopic: [
    #    events.send_affair_created_email_notification,
    #],
    topics.CreateUserTopic: [
        events.create_contact_from_user,
    ],
    topics.MeetingCreatedTopic: [
        events.create_message_from_meeting,
    ],
    topics.UserEventInvitationTopic: [
         # events.send_email_to_user_when_invite_to_an_event,
     ],
}

COMMAND_HANDLERS: Dict[Type[Topic], List[Callable]] = {
    topics.CreateEvenementTopic: [
        commands.create_evenement,
    ],
    topics.CreateMessageTopic: [
        commands.create_message,
    ],
    topics.CreateTagTopic: [
        commands.create_tag,
    ],
    topics.CreateResourceTopic: [
        commands.create_resource,
    ],
    topics.CreateUserTopic: [
        commands.create_user,
    ],
    topics.CreateContactTopic: [
        commands.create_contact,
    ],
    topics.CreateInvitationTopic: [
        commands.create_invitation,
    ],
    topics.CreateMeetingTopic: [
        commands.create_meeting,
    ],
}

HANDLERS: Dict[Type[Topic], List[Callable]] = {**EVENT_HANDLERS, **COMMAND_HANDLERS}
