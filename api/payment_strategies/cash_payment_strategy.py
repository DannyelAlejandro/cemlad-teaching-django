from api.payment_strategies.payment_strategy import PaymentStrategy


class CashPaymentStrategy(PaymentStrategy):
    
    def process_pay(self, cart_id, amount):
        return {
            'method': 'CASH',
            'cart_id': cart_id,
            'amount': float(amount),
            'status': 'completed',
            'message': f'Cash payment of ${amount} processed successfully'
        }
    
    def get_status(self):
        return 'CASH'
