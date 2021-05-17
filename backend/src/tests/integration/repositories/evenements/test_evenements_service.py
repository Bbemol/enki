from datetime import datetime
from uuid import uuid4

import pytest

from domain.evenements.entities.evenement_type import EvenementType
from domain.evenements.entities.evenement_entity import EvenementEntity
from domain.evenements.ports.evenement_repository import AbstractEvenementRepository, AlreadyExistingEvenementUuid, \
    NotFoundEvenement
from .utils import make_evenemnt


def test_add_evenement(evenement_repo: AbstractEvenementRepository):
    uuid = str(uuid4())
    expected_title = "My title"
    expected_description = "My description"
    _type = EvenementType.NATURAL
    started_at = datetime.now()
    creator_id = str(uuid4())
    data = {
        "uuid": uuid,
        "title": expected_title,
        "description": expected_description,
        "type": _type,
        "started_at": started_at,
        "creator_id": creator_id
    }
    evenement = EvenementEntity(**data)
    evenement_repo.add(evenement)

    assert evenement_repo.get_all()[0] == evenement


def test_fails_to_add_evenement_when_already_exists(evenement_repo: AbstractEvenementRepository):
    uuid = str(uuid4())
    data = make_evenemnt(uuid=uuid)
    evenement = EvenementEntity(**data)
    evenement_repo.add(event=evenement)

    with pytest.raises(AlreadyExistingEvenementUuid):
        evenement_repo.add(event=evenement)


def test_list_evenements(evenement_repo: AbstractEvenementRepository):
    evenement1_uuid = str(uuid4())
    serialized_evenement1 = make_evenemnt(uuid=evenement1_uuid)
    evenement = EvenementEntity(**serialized_evenement1)

    evenement_repo.add(evenement)

    evenements = evenement_repo.get_all()

    assert len(evenements) == 1
    assert evenements[0] == evenement

    evenement2_uuid = str(uuid4())
    serialized_evenement2 = make_evenemnt(uuid=evenement2_uuid)
    evenement2 = EvenementEntity(**serialized_evenement2)

    evenement_repo.add(evenement2)

    evenements = evenement_repo.get_all()

    assert len(evenements) == 2
    assert evenements[1] == evenement2


def test_get_by_uuid_when_not_present(evenement_repo: AbstractEvenementRepository):
    with pytest.raises(NotFoundEvenement):
        evenement_repo.get_by_uuid("not_in_repo_uuid")


def test_get_by_uuid_when_evenement_present(evenement_repo: AbstractEvenementRepository):
    evenement1_uuid = str(uuid4())
    serialized_evenement1 = make_evenemnt(evenement1_uuid)
    evenement1 = EvenementEntity(**serialized_evenement1)

    evenement_repo.add(evenement1)
    evenement = evenement_repo.get_by_uuid(evenement1_uuid)
    evenement == evenement1


def two_dict_equality(d1: dict, d2: dict):
    for k, v in d2.items():
        if k == "started_at":
            pass  # TODO: tests date coherence
        else:
            assert d1[k] == d2[k]
