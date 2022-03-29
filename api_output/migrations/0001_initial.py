# Generated by Django 3.2.9 on 2022-03-22 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=30)),
                ('subject', models.CharField(blank=True, max_length=200)),
                ('review', models.TextField(blank=True, max_length=2000, null=True)),
                ('rating', models.FloatField()),
                ('ip', models.CharField(blank=True, max_length=50)),
                ('status', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
