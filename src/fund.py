class Fund:
    def __init__(self,
                 balance: float,
                 nominal_interest_rate: float,
                 compounding_periods: float):
        self.balance = balance
        self.nominal_interest_rate = nominal_interest_rate
        self.compounding_periods = compounding_periods

    def withdraw(self, amount: float) -> None:
        self.balance -= amount

    def deposit(self, amount: float) -> None:
        self.balance += amount

    def effective_interest_rate(self) -> float:
        return (1 +
                self.nominal_interest_rate / self.compounding_periods) ** self.compounding_periods - 1

    def on_pass_years(self, timespan_years: float) -> None:
        self.balance *= (1 +
                         self.effective_interest_rate()) ** timespan_years

    def on_pass_days(self, timespan_days: float) -> None:
        self.on_pass_years(timespan_days / 365)

    def equivalent_value_after_years(self, timespan_years: float) -> float:
        return self.balance * \
            (1 + self.effective_interest_rate()) ** timespan_years

    def __str__(self) -> str:
        return f"Balance: {self.balance}"
