from enum import Enum


class ApplicationType(Enum):
    NORMAL_APPLICATION = "normal_application"
    ECOMMERCE_APPLICATION = "ecommerce_application"


class ApplicationData:
    def __init__(self,
                 id: int = None,
                 name: str = "",
                 description: str = "",
                 application_type: ApplicationType = ApplicationType.NORMAL_APPLICATION
                 ):
        self.id = id
        if name is None or name.strip() == "":
            raise ValueError("name cannot be None or empty")
        self.name = name
        if description is None or description.strip() == "":
            raise ValueError("description cannot be None or empty")
        self.description = description
        if application_type is None:
            raise ValueError("application_type cannot be None")
        self.application_type = application_type if isinstance(application_type, ApplicationType) else ApplicationType(application_type)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "application_type": self.application_type.value if isinstance(self.application_type, ApplicationType) else self.application_type
        }