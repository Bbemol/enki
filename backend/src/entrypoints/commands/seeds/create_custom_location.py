import json
import os
from uuid import uuid4

import click
from flask import current_app
from flask.cli import with_appcontext

from domain.users.entities.group import LocationEntity, LocationType, GroupEntity, GroupType

dir_path = os.path.dirname(os.path.realpath(__file__))

# data from https://github.com/gregoiredavid/france-geojson

@click.command("create-custom-group")
@with_appcontext
def create_custom_group():
    uow = current_app.context
    agglo_aix_marseille = GroupEntity(
        uuid=str(uuid4()),
        label=f"Métropole d'Aix-Marseille-Provence",
        type=GroupType.EPCI
    )
    with uow:
        uow.session.add(agglo_aix_marseille)
        bouche_du_rhone: LocationEntity = uow.session.query(LocationEntity).filter(LocationEntity.external_id == '13').first()
        agglo_aix_marseille.location = bouche_du_rhone