from application.domain.entities.application_data import ApplicationData, ApplicationType
from typing import Optional

from application.infraestructure.repositories.application_data_repository import ApplicationRepository


class ApplicationCommandService:
    def __init__(self, application_repo: ApplicationRepository):
        self.application_repo = application_repo

    def create(self, name: str, description: str, application_type: ApplicationType) -> ApplicationData:
        if not name or not description or application_type is None:
            raise ValueError("All fields are required.")
        application = ApplicationData(
            name=name,
            description=description,
            application_type=application_type
        )
        return self.application_repo.create(application)

    def update(self, application_id: int, name: str, description: str, application_type: ApplicationType) -> Optional[ApplicationData]:
        application = self.application_repo.get_by_id(application_id)
        if not application:
            raise ValueError("Application not found.")
        application.name = name
        application.description = description
        application.application_type = application_type
        return self.application_repo.update(application)

    def delete(self, application_id: int) -> bool:
        return self.application_repo.delete(application_id)
