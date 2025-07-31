from typing import List, Optional
from application.domain.entities.application_data import ApplicationData, ApplicationType
from application.infraestructure.repositories.application_data_repository import ApplicationRepository


class ApplicationQueryService:
    def __init__(self, application_repo: ApplicationRepository):
        self.application_repo = application_repo

    def get_by_id(self, application_id: int) -> Optional[ApplicationData]:
        return self.application_repo.get_by_id(application_id)

    def list_all(self) -> List[ApplicationData]:
        return self.application_repo.get_all()

    def find_by_type_and_name(self, application_type: Optional[ApplicationType] = None, name: Optional[str] = None) -> List[ApplicationData]:
        return self.application_repo.find_by_type_and_name(application_type, name)
