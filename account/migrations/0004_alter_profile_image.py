# Generated by Django 3.2.9 on 2022-03-13 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='media/profile/default.jpg', upload_to='profile'),
        ),
    ]
