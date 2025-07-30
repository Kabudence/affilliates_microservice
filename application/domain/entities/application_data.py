import enum


class ApplicationType(enum):
    EMPRENDEX = "emprendex"
    FULLVENTASGYM = "fullventasgym"


class ApplicationData:
    def __init__(self,
                 id: int = None,
                 name: str = "",
                 description: str = "",
                 application_type: ApplicationType = ApplicationType,
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