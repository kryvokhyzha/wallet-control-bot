from typing import Dict


class User(Dict):
    """
        User structure
    """
    id: int
    username: str
    is_bot: bool
    language_code: str
    budget: float
