from datetime import datetime
from enum import Enum, auto


class TransactionType(Enum):
    INCOME = auto()
    EXPENSE = auto()


class Transaction:
    def __init__(self, transaction_type: TransactionType, amount: float,
                 category: str, description: str = "", date: datetime = None):
        if amount <= 0:
            raise ValueError("Сума транзакції повинна бути більше нуля")

        if not category or category.isspace():
            raise ValueError("Категорія транзакції не може бути порожньою")

        self.transaction_type = transaction_type
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date if date else datetime.now()
        self.created_at = datetime.now()

    def __str__(self) -> str:
        transaction_type_str = "Дохід" if self.transaction_type == TransactionType.INCOME else "Витрата"
        date_str = self.date.strftime("%d.%m.%Y")

        return f"{transaction_type_str}: {self.amount:.2f} - {self.category} ({date_str})"