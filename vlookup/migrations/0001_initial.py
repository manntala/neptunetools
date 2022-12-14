# Generated by Django 3.2.9 on 2022-03-07 22:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedCSVModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('catalog', models.FileField(upload_to='csv/')),
                ('reviews', models.FileField(upload_to='csv/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('activated', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReviewsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_id', models.CharField(blank=True, max_length=100, null=True)),
                ('app_key', models.CharField(blank=True, max_length=100, null=True)),
                ('published', models.CharField(blank=True, max_length=100, null=True)),
                ('review_title', models.CharField(blank=True, max_length=100, null=True)),
                ('review_content', models.CharField(blank=True, max_length=2000, null=True)),
                ('review_score', models.CharField(blank=True, max_length=2, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('user_type', models.CharField(blank=True, max_length=100, null=True)),
                ('sku', models.CharField(blank=True, max_length=100, null=True)),
                ('product_url', models.URLField(blank=True, max_length=1000, null=True)),
                ('product_title', models.CharField(blank=True, max_length=100, null=True)),
                ('product_description', models.CharField(blank=True, max_length=2000, null=True)),
                ('product_image_url', models.URLField(blank=True, max_length=1000, null=True)),
                ('display_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('md_customer_country', models.CharField(blank=True, max_length=100, null=True)),
                ('comment_content', models.CharField(blank=True, max_length=2000, null=True)),
                ('comment_published', models.CharField(blank=True, max_length=100, null=True)),
                ('comment_created', models.CharField(blank=True, max_length=100, null=True)),
                ('review_image', models.URLField(blank=True, max_length=1000, null=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('sub_title', models.CharField(blank=True, max_length=100, null=True)),
                ('int_value', models.CharField(blank=True, max_length=100, null=True)),
                ('string_value', models.CharField(blank=True, max_length=100, null=True)),
                ('pc', models.CharField(blank=True, max_length=100, null=True)),
                ('processed', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CatalogModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(blank=True, max_length=100, null=True)),
                ('product_name', models.CharField(blank=True, max_length=100, null=True)),
                ('product_url', models.URLField(blank=True, max_length=1000, null=True)),
                ('product_image_url', models.URLField(blank=True, max_length=1000, null=True)),
                ('product_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('currency', models.CharField(blank=True, max_length=100, null=True)),
                ('spec_upc', models.CharField(blank=True, max_length=100, null=True)),
                ('spec_mpn', models.CharField(blank=True, max_length=100, null=True)),
                ('spec_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('spec_isbn', models.CharField(blank=True, max_length=100, null=True)),
                ('spec_sku', models.CharField(blank=True, max_length=100, null=True)),
                ('product_tags', models.CharField(blank=True, max_length=100, null=True)),
                ('blacklisted', models.BooleanField(default=False)),
                ('product_group', models.CharField(blank=True, max_length=100, null=True)),
                ('pc', models.CharField(blank=True, max_length=100, null=True)),
                ('processed', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
