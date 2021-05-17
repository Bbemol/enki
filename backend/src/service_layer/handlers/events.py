import os
from datetime import datetime

from flask import current_app

from adapters.http.sge import SgeHelper
from adapters.notifications import email, sms
from domain.core import events
from domain.evenements.services.message_service import MessageService
from domain.users.entities.user import UserEntity
from domain.users.services.contact_service import ContactService
from entrypoints.extensions import email_service
from service_layer.unit_of_work import AbstractUnitOfWork


def send_affair_created_email_notification(event: events.AffairCreatedEvent, **kwargs):
    email.send(
        'mairie@chelles.com',
        f'{event.data.eventId}',
        f'{event.data.primaryAlert.alertCode.whatsHappen.label}'
    )


def send_affair_created_sms_notification(event: events.AffairCreatedEvent, **kwargs):
    sms.send(
        'mairie@chelles.com',
        f'{event.data.eventId}',
        f'{event.data.primaryAlert.alertCode.whatsHappen.label}'
    )


def send_ack_message_to_sge_on_affair_received(event: events.AffairCreatedEvent, **kwargs):
    response = SgeHelper.send_ack_to_sge(event=event)


def create_contact_from_user(event: events.UserCreatedEvent, uow: AbstractUnitOfWork):
    user: UserEntity = event.data
    ContactService.add_contact_from_user(user=user, uow=uow)


def create_message_from_meeting(event: events.MeetingCreatedEvent, uow: AbstractUnitOfWork):
    MessageService.add_message_from_meeting(meeting=event.data, uow=uow)


def send_email_to_user_when_invite_to_an_event(event: events.UserEventInvitationCreated, **kwargs):
    email = event.data["email"]
    evenement_id = event.data["evenement_id"]
    evenement_title = event.data["evenement_title"]
    evenement_url = f"{os.environ.get('ENKI_FRONT_URL')}/evenements/{evenement_id}"
    email_service.send_email(
        to_email=email,
        subject="[Enki] Vous avez été invité à participer à un nouvel évenement",
        template_name="invite_evenement.html",
        evenement_url=evenement_url,
        evenement_title=evenement_title,
        email_receiver=email,
        date=datetime.now()
    )
