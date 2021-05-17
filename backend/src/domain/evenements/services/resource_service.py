from typing import Any, Dict

from werkzeug.exceptions import HTTPException

from domain.evenements.entities.resource import ResourceEntity
from domain.evenements.schemas.resource_schema import ResourceSchema
from service_layer.unit_of_work import AbstractUnitOfWork

class CanDeleteResourceException(HTTPException):
    code = 401
    description = "Action interdite sur cette resource"

class ResourceService:
    schema = ResourceSchema

    @staticmethod
    def add_resource(data: Dict[str, Any], uow: AbstractUnitOfWork) -> Dict[str, Any]:
        schema = ResourceService.schema()
        schema.context = {
            "bucket_name_config": uow.config.MINIO_MESSAGE_RESOURCES_BUCKET
        }
        resource: ResourceEntity = schema.load(data)
        return_value = schema.dump(resource)

        with uow:
            uow.resource.add(resource)

        return return_value

    @staticmethod
    def get_resource(uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            resource: ResourceEntity = uow.resource.get_by_uuid(uuid)
            return_value = ResourceService.schema().dump(resource)

        return return_value

    @staticmethod
    def delete_resource(uuid: str, user_uuid: str, uow: AbstractUnitOfWork) -> bool:
        with uow:
            resource: ResourceEntity = uow.resource.get_by_uuid(uuid)
            if resource.creator_id == user_uuid:
                uow.resource.delete_by_uuid(uuid=uuid)
                return True
            else:
                raise CanDeleteResourceException()
