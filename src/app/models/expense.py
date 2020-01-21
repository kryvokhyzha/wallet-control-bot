from typing import Dict, Optional


class Expense(Dict):
    """
        Expense structure
    """
    user_id: int
    amount: int
    category_name: str
