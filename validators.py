class Validator:

    def is_household_unique(self, name, households):
        for household in households:
            if household.name.lower() == name.lower():
                return False

        return True

    def has_transactions_for_analysis(self, household):
        return household and len(household.transactions) > 0