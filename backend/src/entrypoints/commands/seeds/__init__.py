from .affairs import create_affairs
from .group_and_location import create_group_and_locations
from .position_group import create_position_group
from .create_sdis_groups import create_sdis_groups
from .create_custom_location import create_custom_group

__all__ = [
    create_group_and_locations, create_position_group,
    create_affairs, create_sdis_groups, create_custom_group
]