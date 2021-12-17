import dataclasses


@dataclasses.dataclass
class User:
    id: int
    username: str
    password: str
