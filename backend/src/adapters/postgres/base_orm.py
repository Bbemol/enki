from adapters.postgres.orm.evenements import start_mappers as message_start_mappers
from adapters.postgres.orm.echanges import start_mappers as echanges_start_mappers
from adapters.postgres.orm.metadata import metadata
from adapters.postgres.orm.user_groups import start_mappers as user_start_mappers


def start_mappers():
    user_start_mappers()
    message_start_mappers()
    echanges_start_mappers()
    metadata

