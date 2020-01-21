from typing import Dict, Optional


class Expense(Dict):
    """
        Expense structure
    """
    user_id: int
    amount: float
    category_name: str
