from api.models.product import Product

class ProductRepository:
    
    def find_all_products(self):
        return Product.objects.all()

    def find_product_by_id(self, product_id):
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return None

    def save_product(self, product):
        product.save()
        return product

    def update_product(self, product_id, product_data):
        try:
            product = Product.objects.get(id=product_id)
            for attr, value in product_data.items():
                setattr(product, attr, value)
            product.save()
            return product
        except Product.DoesNotExist:
            return None
    
    def delete_product(self, product_id):
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return True
        except Product.DoesNotExist:
            return False