import json

class CartResponseDTO():
    id = 0
    customer_id = 0
    status = ''
    total = 0.0
    
    def __init__(self, cart):
        self.id = cart.id
        self.customer_id = cart.customer_id
        self.status = cart.status
        self.total = cart.total
    
    def __str__(self):
        return f"Cart(id={self.id}, customer_id='{self.customer_id}', status='{self.status}', total={self.total})"
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'status': self.status,
            'total': float(self.total)
        }
    
    def to_json(self):
        return json.dumps(self.to_dict())