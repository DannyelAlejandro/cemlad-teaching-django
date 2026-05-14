from django.db import models

from api.models.cart import Cart
from api.models.product import Product

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, db_column='cart_id', primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_id', primary_key=True)

    class Meta:
        db_table = 'cart_products'
        managed = False
        unique_together = (('cart', 'product'),)
        constraints = [
            models.UniqueConstraint(fields=['cart', 'product'], name='unique_cart_product')
        ]
    
    def __str__(self):
        return f"CartProduct(cart_id={self.cart.id}, product_id={self.product.id})"