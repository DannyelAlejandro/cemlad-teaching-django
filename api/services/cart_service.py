from decimal import Decimal
from api.repositories.cart_repository import CartRepository
from api.models.cart import Cart
from api.models.cart_product import CartProduct
from api.payment_strategies.payment_strategy_factory import PaymentStrategyFactory


class CartService:
    PAYMENT_METHOD_CASH = 'CASH'
    PAYMENT_METHOD_CARD = 'CARD'
    
    VALID_PAYMENT_METHODS = [PAYMENT_METHOD_CASH, PAYMENT_METHOD_CARD]
    
    def __init__(self):
        self.cart_repository = CartRepository()
        self.payment_factory = PaymentStrategyFactory()
    
    def create_cart(self, cart_data):
        cart = Cart(**cart_data)
        cart.status = "ACT"
        cart.total = Decimal('0.00')
        
        return self.cart_repository.save_cart(cart)
    
    def add_product_to_cart(self, cart_id, product_id):
        cart_product = self.cart_repository.add_product_to_cart(cart_id, product_id)
        
        if cart_product is None:
            return None
        
        cart = self.get_cart_by_id(cart_id)
        if cart:
            self.calculate_cart_total(cart)
            return self.get_cart_by_id(cart_id)
        
        return None
    
    def remove_product_from_cart(self, cart_id, product_id):
        success = self.cart_repository.remove_product_from_cart(cart_id, product_id)
        
        if not success:
            return None
        
        cart = self.get_cart_by_id(cart_id)
        if cart:
            self.calculate_cart_total(cart)
            return self.get_cart_by_id(cart_id)
        
        return None
    
    def get_cart_by_id(self, cart_id):
        return self.cart_repository.find_cart_by_id(cart_id)
    
    def get_cart_by_customer_id(self, customer_id):
        return self.cart_repository.find_cart_by_customer_id(customer_id)
    
    def get_all_carts(self):
        return self.cart_repository.find_all_carts()
    
    def get_products_in_cart(self, cart_id):
        return self.cart_repository.find_products_in_cart(cart_id)
    
    def calculate_cart_total(self, cart):
        if cart is None:
            return None
        
        cart_products = CartProduct.objects.filter(cart_id=cart.id).select_related('product')
        
        total = Decimal('0.00')
        for cart_product in cart_products:
            product = cart_product.product
            if product.price:
                total += Decimal(str(product.price))
        
        cart.total = total
        self.cart_repository.update_cart(cart.id, {'total': total})
        
        return total
    
    def process_payment(self, cart_id, payment_method):
        if payment_method not in self.VALID_PAYMENT_METHODS:
            return None
        
        cart = self.get_cart_by_id(cart_id)
        if not cart:
            return None
        
        try:
            strategy = self.payment_factory.create_strategy(payment_method)
        except ValueError:
            return None
        
        payment_result = strategy.process_pay(cart_id, cart.total)
        
        self.cart_repository.update_cart(cart_id, {'status': 'PAG'})
        
        return payment_result
