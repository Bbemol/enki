from uuid import uuid4
from typing import List
import click
from flask import current_app
from flask.cli import with_appcontext

from domain.users.entities.group import GroupType, PositionGroupTypeEntity


@click.command("create-position-groups")
@with_appcontext
def create_position_group():
    uow = current_app.context
    positions_groups = {
        GroupType.MAIRIE: ["Maire", "Adjoint", "Chef Sécurité", "Gestion des risques", "Sécurité Civile"],
        GroupType.PREFECTURE: ["Préfet", "Directeur de cabinet", "Chef site PC", "Sécurité civile", "Gestion des risques"],
        GroupType.SDIS: ["Directeur", "Responsable CODIS", "Pompier"],
        GroupType.EPCI: ["Gestion des riques", "Sécurité Civile"]
    }


    with uow:

        matches:List[PositionGroupTypeEntity] = uow.session.query(PositionGroupTypeEntity).all()

        def _match(position_label, position_type, position_matches):
            for pos in position_matches:
                if position_type == pos.group_type and position_label == pos.label:
                    return True

            return False

        positions = [PositionGroupTypeEntity(
            uuid=str(uuid4()),
            label=position,
            group_type=group_type
        ) for group_type, positions in positions_groups.items() for position in positions if not _match(position, group_type, matches)]

        uow.session.add_all(positions)
