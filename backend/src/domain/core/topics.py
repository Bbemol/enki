from dataclasses import dataclass
from typing import Any, Callable, Coroutine

EventCallback = Callable[[Any], Coroutine[Any, Any, Any]]


@dataclass
class Topic:
    """

    """
    name: str


@dataclass
class AffairCreatedTopic(Topic):
    name: str = "AffairCreated"


@dataclass
class MessageCreatedTopic(Topic):
    name: str = "MessageCreated"


@dataclass
class UserEventInvitationTopic(Topic):
    name: str = "UserEventInvitation"


@dataclass
class MeetingCreatedTopic(Topic):
    name: str = "MeetingCreated"


@dataclass
class CreateEvenementTopic(Topic):
    name: str = "CreateEvenement"


@dataclass
class CreateMessageTopic(Topic):
    name: str = "CreateMessage"


@dataclass
class CreateTagTopic(Topic):
    name: str = "CreateTag"


@dataclass
class AddTagToMessageTopic(Topic):
    name: str = "AddTagToMessage"


@dataclass
class CreateResourceTopic(Topic):
    name: str = "CreateResource"


@dataclass
class CreateUserTopic(Topic):
    name: str = "CreateUser"


@dataclass
class CreateContactTopic(Topic):
    name: str = "CreateContact"


@dataclass
class CreateInvitationTopic(Topic):
    name: str = "CreateInvitation"


@dataclass
class CreateMeetingTopic(Topic):
    name: str = "CreateMeeting"
