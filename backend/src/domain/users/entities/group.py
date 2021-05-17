from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from dataclasses_json import dataclass_json
from slugify import slugify
from werkzeug.exceptions import HTTPException

from domain.core.entity import Entity


class GroupType(str, Enum):
    MAIRIE = "Mairie"
    PREFECTURE = "Préfecture"
    EPCI = "EPCI"
    PARTENAIRE = "Partenaire"
    SDIS = "Sdis"
    COZ = "Coz"
    COGIC = "Cogic"


class LocationType(str, Enum):
    VILLE = "ville"
    DEPARTEMENT = "departement"
    REGION = "region"
    ZONE = "zone"
    OTHER = "other"


class GroupTypeNotMatchException(HTTPException):
    code = 404
    description = "Group type provided not match"

@dataclass_json
@dataclass
class LocationEntity(Entity):
    label: str
    slug: str = field(init=False)
    search_label: str = field(init=False)
    external_id: str
    type: LocationType
    polygon: Optional[str] = None

    def __post_init__(self):
        self.slug = slugify(self.label)
        self.search_label = f"{self.label} ({self.external_id})"


@dataclass_json
@dataclass
class GroupEntity(Entity):
    label: str
    slug: str = field(init=False)
    type: GroupType
    label_search: Optional[str] = None
    location_id: Optional[str] = None
    location: Optional[LocationEntity] = None

    def __post_init__(self):
        self.slug = slugify(self.label)
        self.label_search = self.label


@dataclass_json
@dataclass
class PositionGroupTypeEntity(Entity):
    label: str
    slug: str = field(init=False)
    group_type: GroupType

    def __post_init__(self):
        self.slug = slugify(self.label)


@dataclass_json
@dataclass
class UserPositionEntity(Entity):
    position_id: str = field(init=False)
    position: PositionGroupTypeEntity = field(init=False)
    group_id: str = field(init=False)
    group: GroupEntity = field(init=False)
