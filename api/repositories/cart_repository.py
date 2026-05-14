from api.models.cart import Cart
from api.models.cart_product import CartProduct
from api.models.product import Product

class CartRepository:
    def save_cart(self, cart):
        cart.save()
        return cart
    
    def add_product_to_cart(self, cart_id, product_id):
        try:
            cart = Cart.objects.get(id=cart_id)
            product = Product.objects.get(id=product_id)
            
            cart_product, created = CartProduct.objects.get_or_create(
                cart_id=cart_id,
                product_id=product_id
            )
            return cart_product
        except Cart.DoesNotExist:
            return None
        except Product.DoesNotExist:
            return None
    
    def remove_product_from_cart(self, cart_id, product_id):
        try:
            cart_product = CartProduct.objects.get(
                cart_id=cart_id,
                product_id=product_id
            )
            cart_product.delete()
            return True
        except CartProduct.DoesNotExist:
            return False
    
    def find_cart_by_id(self, cart_id):
        try:
            return Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            return None
    
    def find_cart_by_customer_id(self, customer_id):
        try:
            return Cart.objects.get(customer_id=customer_id, status="ACT")
        except Cart.DoesNotExist:
            return None
    
    def find_all_carts(self):
        return Cart.objects.all()
    
    def find_products_in_cart(self, cart_id):
        try:
            cart = Cart.objects.get(id=cart_id)
            return CartProduct.objects.filter(cart=cart).select_related('product')
        except Cart.DoesNotExist:
            return None
    
    def update_cart(self, cart_id, cart_data):
        try:
            cart = Cart.objects.get(id=cart_id)
            for attr, value in cart_data.items():
                if hasattr(cart, attr):
                    setattr(cart, attr, value)
            cart.save()
            return cart
        except Cart.DoesNotExist:
            return None
