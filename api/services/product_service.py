from api.repositories.product_repository import ProductRepository
from api.models.product import Product

class ProductService:
    def __init__(self):
        self.product_repository = ProductRepository()
    
    def get_all_products(self):
        return self.product_repository.find_all_products()
    
    def get_product_by_id(self, product_id):
        return self.product_repository.find_product_by_id(product_id)
    
    def create_product(self, product_data):
        product = Product(**product_data)
        return self.product_repository.save_product(product)
    
    def update_product(self, product_id, product_data):
        return self.product_repository.update_product(product_id, product_data)
    
    def delete_product(self, product_id):
        return self.product_repository.delete_product(product_id)