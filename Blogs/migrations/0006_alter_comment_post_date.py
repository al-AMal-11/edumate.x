# Generated by Django 4.1.6 on 2023-04-11 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blogs', '0005_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='post_date',
            field=models.CharField(default='a', max_length=100),
        ),
    ]