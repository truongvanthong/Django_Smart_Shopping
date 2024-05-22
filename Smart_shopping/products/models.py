from django.db import models
from django.conf import settings

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    category_id = models.IntegerField() 
    TGDD_product_link = models.URLField()
    FPT_product_link = models.URLField()
    image = models.URLField()
    TGDD_product_price = models.IntegerField()
    FPT_product_price = models.IntegerField()

    def __str__(self):
        return self.product_name
    
    class Meta:
        db_table = 'product'
        managed = False

class ProductSpec(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(max_length=100)
    screen = models.CharField(max_length=100)
    rear_camera = models.CharField(max_length=100)
    front_camera = models.CharField(max_length=100)
    OS_CPU = models.CharField(max_length=100)
    memory_storage = models.CharField(max_length=100)
    ket_noi = models.CharField(max_length=100)
    pin_sac = models.CharField(max_length=100)
    tien_ich = models.CharField(max_length=100)
    thongtin_chung = models.CharField(max_length=100)

    def __str__(self):
        return self.product.product_name

    class Meta:
        db_table = 'technical_details'
        managed = False

class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name

    class Meta:
        db_table = 'company'
        managed = False

class SentimentManager(models.Manager):
    def filler(self, product_id, company_id):
        return self.filter(product_id=product_id, company_id=company_id)

class Sentiment(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_id')
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='company_id')
    s_pin = models.TextField(null=True)
    s_general = models.TextField(null=True)
    s_service = models.TextField(null=True)
    s_others = models.TextField(null=True)

    objects = SentimentManager()  # Sử dụng custom manager

    def __str__(self):
        return self.product.product_name
    
    class Meta:
        db_table = 'average_sa'
        managed = False

