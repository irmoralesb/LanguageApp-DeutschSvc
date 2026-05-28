from uuid import UUID


class GermanNounNotFoundError(Exception):
    def __init__(self, noun_id: UUID) -> None:
        self.noun_id = noun_id
        super().__init__(f"German noun not found: {noun_id}")


class GermanNounAlreadyExistsError(Exception):
    def __init__(self, singular: str) -> None:
        self.singular = singular
        super().__init__(f"German noun already exists: {singular}")


class GermanNounDataAccessError(Exception):
    def __init__(self) -> None:
        super().__init__("Error accessing German noun data.")
