# Generated by Django 4.1.6 on 2023-04-29 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FrontEnd', '0019_frontend_hero_image_title_frontend_intro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frontend',
            name='intro',
            field=models.FileField(blank=True, null=True, upload_to='intro'),
        ),
    ]