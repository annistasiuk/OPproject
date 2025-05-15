from datetime import datetime
from typing import List, Optional


class Household:
    def __init__(self, name: str, description: str = ""):
        if not name or name.isspace():
            raise ValueError("Назва домогосподарства не може бути порожньою")

        self.name = name
        self.description = description
        self.transactions = []
        self.created_at = datetime.now()

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_transactions(self, start_date: Optional[datetime] = None,
                         end_date: Optional[datetime] = None):
        if start_date is None and end_date is None:
            return self.transactions

        filtered_transactions = []

        for transaction in self.transactions:
            if start_date and transaction.date < start_date:
                continue

            if end_date and transaction.date > end_date:
                continue

            filtered_transactions.append(transaction)

        return filtered_transactions

    def __str__(self) -> str:
        return f"Домогосподарство: {self.name} (транзакцій: {len(self.transactions)})"