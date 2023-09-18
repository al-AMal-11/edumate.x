# Generated by Django 4.1.6 on 2023-04-01 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BackEnd', '0080_salarys_salary_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks_obtained', models.DecimalField(decimal_places=2, max_digits=5)),
                ('total_marks', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pass_fail_status', models.BooleanField()),
                ('grade', models.CharField(max_length=2)),
                ('exam_date', models.DateField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BackEnd.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BackEnd.subject')),
            ],
            options={
                'unique_together': {('student', 'subject')},
            },
        ),
    ]
