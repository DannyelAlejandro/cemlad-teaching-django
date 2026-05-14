from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    
    @abstractmethod
    def process_pay(self, cart_id, amount):
        pass
    
    @abstractmethod
    def get_status(self):
        pass
