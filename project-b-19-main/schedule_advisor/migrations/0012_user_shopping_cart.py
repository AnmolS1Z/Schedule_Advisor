# Generated by Django 4.1.7 on 2023-04-01 22:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule_advisor', '0011_merge_20230401_2205'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='shopping_cart',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='schedule_advisor.shoppingcart'),
        ),
    ]
