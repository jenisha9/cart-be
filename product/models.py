from django.db import models
    
class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.FloatField()
    image = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=100)
    description = models.TextField()
    rating = models.JSONField()

    def __str__(self):
        return self.title