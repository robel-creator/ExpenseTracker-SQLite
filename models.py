class Transaction:
    """Base Class demonstrating Encapsulation."""
    def __init__(self, amount: float, category_id: int, date: str):
        self._amount = amount  # Protected attribute
        self.category_id = category_id
        self.date = date

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if value <= 0:
            raise ValueError("Amount must be greater than zero.")
        self._amount = value

    def get_details(self):
        """Method to be overridden."""
        return f"Transaction: ${self._amount} on {self.date}"


class ExpenseTransaction(Transaction):
    """Derived Class demonstrating Inheritance and Method Overriding."""
    def __init__(self, amount: float, category_id: int, date: str, is_essential: bool = True):
        super().__init__(amount, category_id, date)
        self.is_essential = is_essential

    def get_details(self):
        """Overriding base method."""
        status = "Essential" if self.is_essential else "Non-Essential"
        return f"Expense: ${self._amount} ({status}) on {self.date}"
