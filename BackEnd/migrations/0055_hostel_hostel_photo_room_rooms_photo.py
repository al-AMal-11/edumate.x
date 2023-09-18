# Generated by Django 4.1.6 on 2023-03-06 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BackEnd', '0054_alter_room_fees'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostel',
            name='hostel_photo',
            field=models.ImageField(default='media/user.img', upload_to='media/Hostel_Image'),
        ),
        migrations.AddField(
            model_name='room',
            name='rooms_photo',
            field=models.ImageField(default='media/user.img', upload_to='media/Rooms_Image'),
        ),
    ]