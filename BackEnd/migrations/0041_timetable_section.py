# Generated by Django 4.1.6 on 2023-02-14 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BackEnd', '0040_alter_student_student_feedback_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable',
            name='section',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='BackEnd.section'),
        ),
    ]