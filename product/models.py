from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=255)
    
    
    def __str__(self):
        return self.title
    
class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.FloatField()
    image = models.URLField(blank=True, null=True)
    category = models.ManyToManyField(Category)
    description = models.TextField()
    
    
    def __str__(self):
        return self.title
    
class Rate(models.Model):
    rate = models.DecimalField(max_digits=2, decimal_places=1)
    count = models.IntegerField(default=0)