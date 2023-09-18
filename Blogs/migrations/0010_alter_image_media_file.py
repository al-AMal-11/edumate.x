# Generated by Django 4.1.6 on 2023-04-20 10:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blogs', '0009_remove_image_image_file_image_media_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='media_file',
            field=models.FileField(upload_to='Blog_media/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi', 'jpg', 'jpeg', 'png'])]),
        ),
    ]