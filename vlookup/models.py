from django.db import models
from account.models import Account

class CatalogModel(models.Model):
    
    product_id = models.CharField(max_length=100, blank=True, null=True)
    product_name = models.CharField(max_length=100, blank=True, null=True)
    product_url = models.URLField(max_length=1000, blank=True, null=True)
    product_image_url = models.URLField(max_length=1000, blank=True, null=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=100, blank=True, null=True)
    spec_upc = models.CharField(max_length=100, blank=True, null=True)
    spec_mpn = models.CharField(max_length=100, blank=True, null=True)
    spec_brand = models.CharField(max_length=100, blank=True, null=True)
    spec_isbn = models.CharField(max_length=100, blank=True, null=True)
    spec_sku = models.CharField(max_length=100, blank=True, null=True)
    product_tags = models.CharField(max_length=100, blank=True, null=True)
    blacklisted = models.BooleanField(default=False)
    product_group = models.CharField(max_length=100, blank=True, null=True)
    
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    pc = models.CharField(max_length=100, blank=True, null=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.owner} - {self.product_id}"

class ReviewsModel(models.Model):
    
    review_id = models.CharField(max_length=100, blank=True, null=True)
    app_key = models.CharField(max_length=100, blank=True, null=True)
    published = models.CharField(max_length=100, blank=True, null=True)
    review_title = models.CharField(max_length=100, blank=True, null=True)
    review_content = models.CharField(max_length=2000, blank=True, null=True)
    review_score = models.CharField(max_length=2, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    user_type = models.CharField(max_length=100, blank=True, null=True)
    sku = models.CharField(max_length=100, blank=True, null=True)
    product_url = models.URLField(max_length=1000, blank=True, null=True)
    product_title = models.CharField(max_length=100, blank=True, null=True)
    product_description = models.CharField(max_length=2000, blank=True, null=True)
    product_image_url = models.URLField(max_length=1000, blank=True, null=True)
    display_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    md_customer_country = models.CharField(max_length=100, blank=True, null=True)
    comment_content = models.CharField(max_length=2000, blank=True, null=True)
    comment_published = models.CharField(max_length=100, blank=True, null=True)
    comment_created = models.CharField(max_length=100, blank=True, null=True)
    review_image = models.URLField(max_length=1000, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    sub_title = models.CharField(max_length=100, blank=True, null=True)
    int_value = models.CharField(max_length=100, blank=True, null=True)
    string_value = models.CharField(max_length=100, blank=True, null=True)

    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    pc = models.CharField(max_length=100, blank=True, null=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.owner} - {self.sku} - {self.review_id} - {self.processed}"

class UploadedCSVModel(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    catalog = models.FileField(upload_to='csv/')
    reviews = models.FileField(upload_to='csv/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.catalog} {self.reviews}" 
