# from django.contrib.auth.models import Account
from django.db import models
from account.models import Account

class OrderProcessModel(models.Model):
    
    order_id = models.CharField(max_length=100, blank=True, null=True)
    order_date = models.DateTimeField(blank=True, null=True)
    external_id = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    product_id = models.CharField(max_length=100, blank=True, null=True)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.owner} - {self.first_name} {self.last_name} - {self.order_id}"

class Csv(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=100, blank=True, null=True)
    file_name = models.FileField(upload_to='csv/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.file_name}"
    
class OrderTemplate(models.Model):
    order_template = models.FileField(upload_to='save/', default='save/order_template.csv')

    def __str__(self):
        return f"File id: {self.id} - {self.order_template}"

class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

class GetKey(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    appkey = models.CharField(max_length=100, unique=True)
    secretkey = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.token



