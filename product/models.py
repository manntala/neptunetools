from django.db import models
from account.models import Account

class UploadCsvModel(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=100, blank=True, null=True)
    product = models.FileField(upload_to='csv/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.product}"

class UpdateProductModel(models.Model):
    yotpo_id = models.CharField(max_length=100, blank=True, null=True)
    external_id = models.CharField(max_length=100, blank=True, null=True)
    product_title = models.CharField(max_length=100, blank=True, null=True)
    product_url = models.CharField(max_length=100, blank=True, null=True)
    product_image_url = models.CharField(max_length=100, blank=True, null=True)
    product_price = models.IntegerField(blank=True, null=True)
    product_currency = models.CharField(max_length=100, blank=True, null=True)
    upc = models.CharField(max_length=100, blank=True, null=True)
    mpn = models.CharField(max_length=100, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    isbn = models.CharField(max_length=100, blank=True, null=True)
    sku = models.CharField(max_length=100, blank=True, null=True)
    product_tags = models.CharField(max_length=100, blank=True, null=True)
    blacklisted = models.BooleanField(default=False)
    product_group = models.CharField(max_length=100, blank=True, null=True)

    processed = models.BooleanField(default=False)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.external_id} - {self.product_title}"

class AddProductModel(models.Model):
    external_id = models.CharField(max_length=100, blank=True, null=True)
    product_title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    product_url = models.CharField(max_length=100, blank=True, null=True)
    product_price = models.IntegerField(blank=True, null=True)
    sku = models.CharField(max_length=100, blank=True, null=True)

    processed = models.BooleanField(default=False)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.external_id} - {self.product_title}"