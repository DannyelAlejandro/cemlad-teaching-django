from api.payment_strategies.payment_strategy import PaymentStrategy


class CardPaymentStrategy(PaymentStrategy):
    
    def process_pay(self, cart_id, amount):
        return {
            'method': 'CARD',
            'cart_id': cart_id,
            'amount': float(amount),
            'status': 'completed',
            'message': f'Card payment of ${amount} processed successfully'
        }
    
    def get_status(self):
        return 'CARD'
