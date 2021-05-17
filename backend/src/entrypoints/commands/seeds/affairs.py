import json
import click
import os
import random
from datetime import datetime
from typing import List
from uuid import uuid4
from cisu.entities.commons import Severity, CoordType, LocationType
from cisu.entities.commons.location_type import LocationShape
from cisu.factories.alert_factory import PrimaryAlertFactory
from cisu.entities.alert_entity import AlertCode
from cisu.factories.alert_factory import PrimaryAlertFactory, CallFactory, CallerFactory, CallTakerFactory
from cisu.factories.alert_code_factory import AlertCodeFactory, WhatsHappenFactory, LocationKindFactory, \
    RiskThreatFactory, HealthMotiveFactory,VictimsFactory
from cisu.entities.alert_entity import PrimaryAlertEntity
from cisu.factories.location_factory import LocationTypeFactory
from cisu.factories.uid_factory import UidFactory
from cisu.entities.commons.common_alerts import Reporting, AlertId, Call, \
    Caller, CallTaker, AnyURI, Language,Version
from cisu.constants.constants import RiskThreatConstants, HealthMotiveConstants, \
    LocationKindConstants, WhatsHappenConstants
from flask import current_app
from flask.cli import with_appcontext
from shapely.geometry import Polygon, Point

from domain.affairs.entities.affair_entity import AffairEntity
from domain.affairs.entities.simple_affair_entity import SimpleAffairEntity
from domain.evenements.entities.evenement_type import EvenementType, EVENEMENT_TYPE_TO_CISU_CODE


dir_path = os.path.dirname(os.path.realpath(__file__))


def generate_random(number: int, polygon: Polygon):
    points = []
    minx, miny, maxx, maxy = polygon.bounds
    while len(points) < number:
        pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if polygon.contains(pnt):
            points.append(pnt)
    return points


@click.command("create-affairs")
@click.option('--number', type=int, default=10)
@click.option('--insee_code', type=str)
@click.option('--dept_code', type=str)
@click.option('--event_type', type=click.Choice(list(EvenementType), case_sensitive=False))
@with_appcontext
def create_affairs(number: int, event_type:EvenementType, insee_code: str = None, dept_code: str = None, ):

    uow = current_app.context

    communes_path = dir_path + "/data/communes-version-simplifiee.geojson"
    dept_path = dir_path + "/data/departements-version-simplifiee.geojson"

    if insee_code:
        with open(communes_path) as f:
            data = json.load(f)["features"]
        code = insee_code
    elif dept_code:
        with open(dept_path) as f:
            data = json.load(f)["features"]
        code = dept_code

    else:
        code = "77"
        with open(dept_path) as f:
            data = json.load(f)["features"]

    selected_shape = [feature for feature in data if feature["properties"]["code"] == code][0]
    polygon = Polygon(selected_shape["geometry"]["coordinates"][0])
    points: List[Point] = generate_random(number=number, polygon=polygon)
    whats_happen_codes = [random.choice(EVENEMENT_TYPE_TO_CISU_CODE.get(event_type)) for _ in range(len(points))]
    affairs = []
    for point, whatsHappenCode in zip(points,whats_happen_codes)     :
        affair = AffairEntity(
            eventId=UidFactory().build(),
            createdAt=datetime.now(),
            severity=Severity.random(),
            eventLocation=LocationType(
                name="ok",
                address=["test"],
                coord=CoordType(point.y, point.x, height=0),
                type=LocationShape.POINT
            ),
            primaryAlert=PrimaryAlertEntity(
                alertId=AlertId(UidFactory().build()),
                receivedAt=datetime.utcnow(),
                reporting=Reporting.random(),
                alertInformation="C'est une information concernant l'alerte",
                alertLocation=LocationTypeFactory().build(),
                call=CallFactory().build(),
                caller=CallerFactory().build(),
                callTaker=CallTakerFactory().build(),
                resource=[],
                alertCode=AlertCode(
                    version=Version("latest"),
                    whatsHappen=WhatsHappenConstants().get_by_code(whatsHappenCode),
                    locationKind=LocationKindFactory().build(),
                    riskThreat=RiskThreatFactory().build(),
                    healthMotive=HealthMotiveFactory().build(),
                    victims=VictimsFactory().build(),
                ),
                primary=True
            ),

            otherAlert=[],
        )
        simple_affair_entity: SimpleAffairEntity = SimpleAffairEntity(
            uuid=str(uuid4()),
            sge_hub_id=affair.uuid,
            default_affair=affair
        )
        affairs.append(simple_affair_entity)
    with uow:
        uow.session.add_all(affairs)
