# Generated by Django 4.1.7 on 2023-04-03 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule_advisor', '0017_rename_statues_user_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.IntegerField(default=-2),
        ),
    ]
