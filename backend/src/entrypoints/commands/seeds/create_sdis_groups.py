import json
import os
from uuid import uuid4
from typing import List
import click
from flask import current_app
from flask.cli import with_appcontext

from domain.users.entities.group import LocationEntity, LocationType, GroupEntity, GroupType

dir_path = os.path.dirname(os.path.realpath(__file__))

# data from https://github.com/gregoiredavid/france-geojson

mapping = {'Ain': "de l'", 'Aisne': "de l'", 'Allier': "de l'", 'Alpes-de-Haute-Provence': 'des ',
           'Hautes-Alpes': 'des ', 'Alpes-Maritimes': 'des ', 'Ardèche': "de l'", 'Ardennes': 'des ', 'Ariège': "de l'",
           'Aube': "de l'", 'Aude': "de l'", 'Aveyron': "de l'", 'Bouches-du-Rhône': 'des ', 'Calvados': 'du ',
           'Cantal': 'du ', 'Charente': 'de ', 'Charente-Maritime': 'de ', 'Cher': 'du ', 'Corrèze': 'de la ',
           "Côte-d'Or": 'de ', "Côtes-d'Armor": 'des ', 'Creuse': 'de la ', 'Dordogne': 'de ', 'Doubs': 'du ',
           'Drôme': 'de la ', 'Eure': "de l'", 'Eure-et-Loir': "d'", 'Finistère': 'du ', 'Corse-du-Sud': 'de ',
           'Haute-Corse': 'de ', 'Gard': 'du ', 'Haute-Garonne': 'de ', 'Gers': 'du ', 'Gironde': 'de ',
           'Hérault': "de l'", 'Ille-et-Vilaine': "d'", 'Indre': "de l'", 'Indre-et-Loire': "de l'", 'Isère': "de l'",
           'Jura': 'du ', 'Landes': 'des ', 'Loir-et-Cher': 'du ', 'Loire': 'de la ', 'Haute-Loire': 'de ',
           'Loire-Atlantique': 'de ', 'Loiret': 'du ', 'Lot': 'du ', 'Lot-et-Garonne': 'du ', 'Lozère': 'de la ',
           'Maine-et-Loire': 'du ', 'Manche': 'de la ', 'Marne': 'de la ', 'Haute-Marne': 'de la ', 'Mayenne': 'de ',
           'Meurthe-et-Moselle': 'de ', 'Meuse': 'de la ', 'Morbihan': 'du ', 'Moselle': 'de ', 'Nièvre': 'de la ',
           'Nord': 'du ', 'Oise': "de l'", 'Orne': "de l'", 'Pas-de-Calais': 'du ', 'Puy-de-Dôme': 'du ',
           'Pyrénées-Atlantiques': 'des ', 'Hautes-Pyrénées': 'des ', 'Pyrénées-Orientales': 'des ', 'Bas-Rhin': 'du ',
           'Haut-Rhin': 'du ', 'Rhône': 'du ', 'Haute-Saône': 'de ', 'Saône-et-Loire': 'de ', 'Sarthe': 'de la ',
           'Savoie': 'de ', 'Haute-Savoie': 'de ', 'Paris': 'de ', 'Seine-Maritime': 'de ', 'Seine-et-Marne': 'de ',
           'Yvelines': 'des ', 'Deux-Sèvres': 'des ', 'Somme': 'de la ', 'Tarn': 'du ', 'Tarn-et-Garonne': 'du ',
           'Var': 'du ', 'Vaucluse': 'du ', 'Vendée': 'de ', 'Vienne': 'de la ', 'Haute-Vienne': 'de la ',
           'Vosges': 'des ', 'Yonne': "de l'", 'Territoire de Belfort': 'du ', 'Essonne': "de l'",
           'Hauts-de-Seine': 'des ', 'Seine-Saint-Denis': 'de ', 'Val-de-Marne': 'du ', "Val-d'Oise": 'du '}


def _build_polygon_from_coordinates(coordinates):
    polygon_value = f"POLYGON(({' ,'.join([' '.join([str(e[1]), str(e[0])]) for e in coordinates])}))"
    if "[" in polygon_value:
        return None
    return polygon_value


@click.command("create-sdis")
@with_appcontext
def create_sdis_groups():
    uow = current_app.context

    with uow:
        depts:List[LocationEntity] = uow.session.query(LocationEntity).filter(
            LocationEntity.type == LocationType.DEPARTEMENT).all()
        sdis_groups_already_in: List[GroupEntity] = uow.session.query(GroupEntity).filter(
            GroupEntity.type == GroupType.SDIS).all()

        def _match(label, matches : List[GroupEntity]):
            for match in matches:
                if match.type == GroupType.SDIS and label == label:
                    return True

            return False

        sdis_groups = [
            GroupEntity(
                uuid=str(uuid4()),
                label=f"Sdis {mapping[dept.label]}{dept.label}",
                type=GroupType.SDIS
            )
            for dept in depts #if _match(f"Sdis {mapping[dept.label]}{dept.label}", sdis_groups_already_in)
        ]

        uow.session.add_all(sdis_groups)
        for sdis, match in zip(sdis_groups, depts):
            sdis.location = match
