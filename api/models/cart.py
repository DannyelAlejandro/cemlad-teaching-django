from django.db import models

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.IntegerField()
    status = models.CharField(max_length=3)
    total = models.DecimalField(max_digits=18, decimal_places=2)
    
    class Meta:
        db_table = 'carts'
        managed = False
    
    def __str__(self):
        return f"Cart(id={self.id}, customer_id='{self.customer_id}', status='{self.status}', total={self.total})"
