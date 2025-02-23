from django.db import models

# Create your models here.
class ProductWatch(models.Model):
    plateform = models.IntegerField(default=1)
    url = models.TextField()
    name = models.CharField(max_length=255, null=True, blank=True, default=None)
    is_active = models.BooleanField(default=True)

class ProductHistory(models.Model):
    product_watch = models.ForeignKey(ProductWatch, on_delete=models.CASCADE, related_name="history")
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)