# Generated by Django 3.2.9 on 2022-03-22 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_output', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewrating',
            name='name',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
