from uuid import UUID


class GermanVerbNotFoundError(Exception):
    def __init__(self, verb_id: UUID) -> None:
        self.verb_id = verb_id
        super().__init__(f"German verb not found: {verb_id}")


class GermanVerbAlreadyExistsError(Exception):
    def __init__(self, infinitive: str) -> None:
        self.infinitive = infinitive
        super().__init__(f"German verb already exists: {infinitive}")


class GermanVerbDataAccessError(Exception):
    def __init__(self) -> None:
        super().__init__("Error accessing German verb data.")
