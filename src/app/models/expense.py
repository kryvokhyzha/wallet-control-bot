from typing import Dict, Optional


class Expense(Dict):
    """
        Expense structure
    """
    id: Optional[int]
    amount: int
    category_name: str
