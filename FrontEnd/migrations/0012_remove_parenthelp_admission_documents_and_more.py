# Generated by Django 4.1.6 on 2023-04-29 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FrontEnd', '0011_delete_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parenthelp',
            name='admission_documents',
        ),
        migrations.RemoveField(
            model_name='parenthelp',
            name='admission_status',
        ),
    ]