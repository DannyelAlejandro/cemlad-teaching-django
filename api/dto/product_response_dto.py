import json

class ProductResponseDTO():
    id = 0
    name = ''
    code = ''
    price = 0.0
    
    def __init__(self, product):
        self.id = product.id
        self.name = product.name
        self.code = product.code
        self.price = product.price
    
    def __str__(self):
        return f"ProductResponseDTO(id={self.id}, name='{self.name}', code='{self.code}', price={self.price})"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'price': self.price
        }
    
    def to_json(self):
        return json.dumps(self.to_dict())