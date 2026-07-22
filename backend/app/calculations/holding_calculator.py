from decimal import Decimal

from app.models.transaction import Transaction
from app.schemas.holding import HoldingResponse


class HoldingCalculator:
    """Calculate holdings from account transactions."""

    @staticmethod
    def calculate(
        transactions: list[Transaction],
    ) -> list[HoldingResponse]:
        holdings: dict[str, dict[str, Decimal | str]] = {}

        for transaction in transactions:
            if transaction.symbol is None:
                continue

            symbol = transaction.symbol

            if symbol not in holdings:
                holdings[symbol] = {
                    "quantity": Decimal("0"),
                    "total_cost": Decimal("0"),
                    "currency": transaction.currency,
                }

            quantity = transaction.quantity or Decimal("0")
            price = transaction.price or Decimal("0")
            fees = transaction.fees or Decimal("0")

            if transaction.transaction_type.name == "BUY":
                holdings[symbol]["quantity"] += quantity
                holdings[symbol]["total_cost"] += (quantity * price) + fees

            elif transaction.transaction_type.name == "SELL":
                current_quantity = holdings[symbol]["quantity"]

                if current_quantity == 0:
                    continue

                average_cost = holdings[symbol]["total_cost"] / current_quantity

                holdings[symbol]["quantity"] -= quantity
                holdings[symbol]["total_cost"] -= average_cost * quantity

        results: list[HoldingResponse] = []

        for symbol, holding in holdings.items():
            quantity = holding["quantity"]

            if quantity <= 0:
                continue

            total_cost = holding["total_cost"]
            average_cost = total_cost / quantity

            results.append(
                HoldingResponse(
                    symbol=symbol,
                    quantity=quantity,
                    average_cost=average_cost,
                    cost_basis=total_cost,
                    currency=holding["currency"],
                )
            )

        return results
