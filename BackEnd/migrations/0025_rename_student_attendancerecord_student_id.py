# Generated by Django 4.1.5 on 2023-01-26 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BackEnd', '0024_attendancerecord'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendancerecord',
            old_name='student',
            new_name='student_id',
        ),
    ]