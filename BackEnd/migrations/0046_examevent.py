# Generated by Django 4.1.6 on 2023-02-20 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BackEnd', '0045_remove_timetable_other'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField()),
                ('StartTime', models.TimeField()),
                ('RoomNO', models.CharField(max_length=100)),
                ('end_time', models.TimeField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now_add=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BackEnd.section')),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BackEnd.staff')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BackEnd.subject')),
            ],
        ),
    ]