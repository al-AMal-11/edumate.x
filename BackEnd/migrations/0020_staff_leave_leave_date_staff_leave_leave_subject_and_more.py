# Generated by Django 4.1.5 on 2023-01-13 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BackEnd', '0019_remove_staff_leave_leave_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff_leave',
            name='leave_date',
            field=models.CharField(default='i', max_length=100),
        ),
        migrations.AddField(
            model_name='staff_leave',
            name='leave_subject',
            field=models.CharField(default='iam', max_length=100),
        ),
        migrations.AddField(
            model_name='student_leave',
            name='leave_date',
            field=models.CharField(default='iam', max_length=100),
        ),
        migrations.AddField(
            model_name='student_leave',
            name='leave_subject',
            field=models.CharField(default='iamam', max_length=100),
        ),
    ]
