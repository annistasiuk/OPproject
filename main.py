import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from household import Household
from transaction import Transaction, TransactionType
from finance_analyzer import FinanceAnalyzer
from validators import Validator


class FinanceManagerApp:

    def __init__(self):
        self.households = []
        self.current_household = None
        self.validator = Validator()

    def display_menu(self):
        print("\n===== СИСТЕМА КЕРУВАННЯ ФІНАНСАМИ ДОМОГОСПОДАРСТВ =====")
        print("1. Створити нове домогосподарство")
        print("2. Вибрати існуюче домогосподарство")
        print("3. Додати транзакцію")
        print("4. Переглянути всі транзакції")
        print("5. Створити фінансовий звіт")
        print("0. Вихід")
        print("======================================================")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Оберіть опцію (0-5): ")

            if choice == "0":
                print("Дякуємо за використання системи. До побачення!")
                break
            elif choice == "1":
                self.create_household()
            elif choice == "2":
                self.select_household()
            elif choice == "3":
                self.add_transaction()
            elif choice == "4":
                self.view_transactions()
            elif choice == "5":
                self.create_financial_report()
            else:
                print("Невірний вибір. Спробуйте ще раз.")

    def create_household(self):
        name = input("Введіть назву домогосподарства: ")

        if not self.validator.is_household_unique(name, self.households):
            print(f"Домогосподарство з назвою '{name}' вже існує.")
            return

        description = input("Введіть опис домогосподарства (необов'язково): ")

        try:
            household = Household(name, description)
            self.households.append(household)
            self.current_household = household
            print(f"Домогосподарство '{name}' успішно створено і вибрано.")
        except ValueError as e:
            print(f"Помилка при створенні домогосподарства: {e}")

    def select_household(self):
        if not self.households:
            print("Немає зареєстрованих домогосподарств. Створіть нове.")
            return

        print("\nДоступні домогосподарства:")
        for idx, household in enumerate(self.households, 1):
            print(f"{idx}. {household.name}")

        try:
            choice = int(input("Виберіть номер домогосподарства: "))
            if 1 <= choice <= len(self.households):
                self.current_household = self.households[choice - 1]
                print(f"Вибрано домогосподарство '{self.current_household.name}'.")
            else:
                print("Невірний номер. Спробуйте ще раз.")
        except ValueError:
            print("Будь ласка, введіть число.")

    def add_transaction(self):
        if not self.current_household:
            print("Спочатку виберіть або створіть домогосподарство.")
            return

        print("\nДодавання нової транзакції")
        print("Тип транзакції:")
        print("1. Дохід")
        print("2. Витрата")

        try:
            type_choice = int(input("Виберіть тип (1-2): "))
            if type_choice == 1:
                transaction_type = TransactionType.INCOME
            elif type_choice == 2:
                transaction_type = TransactionType.EXPENSE
            else:
                print("Невірний вибір. Повернення до головного меню.")
                return

            amount = float(input("Введіть суму: "))
            if amount <= 0:
                print("Сума повинна бути більше нуля.")
                return

            category = input("Введіть категорію (наприклад, 'Зарплата', 'Продукти'): ")
            description = input("Введіть опис (необов'язково): ")

            date_str = input("Введіть дату (формат: ДД.ММ.РРРР) або залиште порожнім для поточної дати: ")
            if date_str:
                try:
                    date = datetime.strptime(date_str, "%d.%m.%Y")
                except ValueError:
                    print("Невірний формат дати. Використано поточну дату.")
                    date = datetime.now()
            else:
                date = datetime.now()

            transaction = Transaction(
                transaction_type=transaction_type,
                amount=amount,
                category=category,
                description=description,
                date=date
            )

            self.current_household.add_transaction(transaction)
            print("Транзакцію успішно додано.")

        except ValueError as e:
            print(f"Помилка при додаванні транзакції: {e}")

    def view_transactions(self):
        if not self.current_household:
            print("Спочатку виберіть або створіть домогосподарство.")
            return

        transactions = self.current_household.transactions
        if not transactions:
            print(f"У домогосподарстві '{self.current_household.name}' немає транзакцій.")
            return

        print(f"\nТранзакції домогосподарства '{self.current_household.name}':")
        print("-" * 80)
        print(f"{'#':<3} {'Тип':<10} {'Сума':<10} {'Категорія':<15} {'Дата':<12} {'Опис':<30}")
        print("-" * 80)

        for idx, transaction in enumerate(transactions, 1):
            type_str = "Дохід" if transaction.transaction_type == TransactionType.INCOME else "Витрата"
            date_str = transaction.date.strftime("%d.%m.%Y")
            print(
                f"{idx:<3} {type_str:<10} {transaction.amount:<10.2f} {transaction.category:<15} {date_str:<12} {transaction.description[:30]:<30}")

    def create_financial_report(self):
        if not self.current_household:
            print("Спочатку виберіть або створіть домогосподарство.")
            return

        analyzer = FinanceAnalyzer()

        try:
            report = analyzer.generate_report(self.current_household)

            print(f"\nФінансовий звіт для '{self.current_household.name}'")
            print("=" * 50)
            print(f"Загальний дохід: {report['total_income']:.2f}")
            print(f"Загальні витрати: {report['total_expenses']:.2f}")
            print(f"Баланс: {report['balance']:.2f}")

            print("\nДоходи за категоріями:")
            for category, amount in report['income_by_category'].items():
                print(f"- {category}: {amount:.2f}")

            print("\nВитрати за категоріями:")
            for category, amount in report['expenses_by_category'].items():
                print(f"- {category}: {amount:.2f}")

        except ValueError as e:
            print(f"Помилка при створенні звіту: {e}")


if __name__ == "__main__":
    app = FinanceManagerApp()
    app.run()