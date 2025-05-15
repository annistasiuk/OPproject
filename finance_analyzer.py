from collections import defaultdict
from transaction import TransactionType


class FinanceAnalyzer:
    def generate_report(self, household):
        if not self._has_transactions(household):
            raise ValueError(f"Домогосподарство '{household.name}' не має транзакцій для аналізу")

        total_income = 0
        total_expenses = 0
        income_by_category = defaultdict(float)
        expenses_by_category = defaultdict(float)

        for transaction in household.transactions:
            if transaction.transaction_type == TransactionType.INCOME:
                total_income += transaction.amount
                income_by_category[transaction.category] += transaction.amount
            else:
                total_expenses += transaction.amount
                expenses_by_category[transaction.category] += transaction.amount

        report = {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'balance': total_income - total_expenses,
            'income_by_category': dict(income_by_category),
            'expenses_by_category': dict(expenses_by_category)
        }

        return report

    def _has_transactions(self, household):
        return len(household.transactions) > 0

    def get_top_expense_categories(self, household, limit=5):
        if not self._has_transactions(household):
            return []

        expenses_by_category = defaultdict(float)

        for transaction in household.transactions:
            if transaction.transaction_type == TransactionType.EXPENSE:
                expenses_by_category[transaction.category] += transaction.amount

        sorted_categories = sorted(
            expenses_by_category.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_categories[:limit]

    def get_top_income_categories(self, household, limit=5):
        if not self._has_transactions(household):
            return []

        income_by_category = defaultdict(float)

        for transaction in household.transactions:
            if transaction.transaction_type == TransactionType.INCOME:
                income_by_category[transaction.category] += transaction.amount

        sorted_categories = sorted(
            income_by_category.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_categories[:limit]