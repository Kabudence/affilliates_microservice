from typing import Optional, List

from application.domain.entities.application_data import ApplicationData, ApplicationType
from application.infraestructure.model.application_data_model import ApplicationModel


class ApplicationRepository:
    def get_by_id(self, id: int) -> Optional[ApplicationData]:
        try:
            record = ApplicationModel.get(ApplicationModel.id == id)
            return ApplicationData(
                id=record.id,
                name=record.name,
                description=record.description,
                application_type=ApplicationType(record.application_type),
            )
        except ApplicationModel.DoesNotExist:
            return None

    def get_all(self) -> List[ApplicationData]:
        return [
            ApplicationData(
                id=rec.id,
                name=rec.name,
                description=rec.description,
                application_type=ApplicationType(rec.application_type),

            )
            for rec in ApplicationModel.select()
        ]

    def create(self, application: ApplicationData) -> ApplicationData:
        record = ApplicationModel.create(
            name=application.name,
            description=application.description,
            application_type=application.application_type.value if isinstance(application.application_type, ApplicationType) else application.application_type
        )
        return ApplicationData(
            id=record.id,
            name=record.name,
            description=record.description,
            application_type=ApplicationType(record.application_type),

        )

    def update(self, application: ApplicationData) -> Optional[ApplicationData]:
        try:
            record = ApplicationModel.get(ApplicationModel.id == application.id)
            record.name = application.name
            record.description = application.description
            record.application_type = application.application_type.value if isinstance(application.application_type, ApplicationType) else application.application_type
            record.save()
            return ApplicationData(
                id=record.id,
                name=record.name,
                description=record.description,
                application_type=ApplicationType(record.application_type),

            )
        except ApplicationModel.DoesNotExist:
            return None

    def delete(self, application_id: int) -> bool:
        try:
            record = ApplicationModel.get(ApplicationModel.id == application_id)
            record.delete_instance()
            return True
        except ApplicationModel.DoesNotExist:
            return False

    # Buscar por tipo de aplicación y/o nombre
    def find_by_type_and_name(self, application_type: Optional[ApplicationType] = None, name: Optional[str] = None) -> List[ApplicationData]:
        query = ApplicationModel.select()
        if application_type is not None:
            query = query.where(ApplicationModel.application_type == application_type.value if isinstance(application_type, ApplicationType) else application_type)
        if name is not None:
            query = query.where(ApplicationModel.name == name)
        return [
            ApplicationData(
                id=rec.id,
                name=rec.name,
                description=rec.description,
                application_type=ApplicationType(rec.application_type),

            )
            for rec in query
        ]
