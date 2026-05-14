import json


class PaymentResponseDTO:    
    def __init__(self, message: str):
        self.message = message
    
    def __str__(self):
        return f"PaymentResponseDTO(message='{self.message}')"
    
    def to_dict(self):
        return {
            'message': self.message
        }
    
    def to_json(self):
        return json.dumps(self.to_dict())
