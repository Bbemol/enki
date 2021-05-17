from datetime import datetime

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

from domain.core.entity import Entity


@dataclass_json
@dataclass
class EchangeEntity(Entity):
    """

    """

    uuid: str
    payload: str
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())