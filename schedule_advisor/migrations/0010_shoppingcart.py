# Generated by Django 4.1.7 on 2023-03-30 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule_advisor', '0009_alter_course_class_nbr'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courses', models.ManyToManyField(to='schedule_advisor.course')),
            ],
        ),
    ]
