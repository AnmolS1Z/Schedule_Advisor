# Generated by Django 4.1.7 on 2023-03-19 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule_advisor', '0007_subject_descr'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='section_type',
            field=models.CharField(default='Lecture', max_length=10),
        ),
    ]
