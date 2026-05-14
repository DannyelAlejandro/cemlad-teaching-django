from django.db import models

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)
    price = models.DecimalField(max_digits=18, decimal_places=2)
    
    class Meta:
        db_table = 'products'
        managed = False
    
    def __str__(self):
        return f"Product(id={self.id}, name='{self.name}', code='{self.code}', price={self.price})"