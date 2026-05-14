from api.payment_strategies.payment_strategy import PaymentStrategy
from api.payment_strategies.cash_payment_strategy import CashPaymentStrategy
from api.payment_strategies.card_payment_strategy import CardPaymentStrategy
from api.payment_strategies.payment_constants import PAYMENT_METHOD_CASH, PAYMENT_METHOD_CARD


class PaymentStrategyFactory:
    @staticmethod
    def create_strategy(payment_method: str) -> PaymentStrategy:
        payment_method = payment_method.upper()
        
        if payment_method == PAYMENT_METHOD_CASH:
            return CashPaymentStrategy()
        elif payment_method == PAYMENT_METHOD_CARD:
            return CardPaymentStrategy()
        else:
            raise ValueError(f"Payment method not valid: {payment_method}. "
                           f"Use 'CASH' or 'CARD'")
