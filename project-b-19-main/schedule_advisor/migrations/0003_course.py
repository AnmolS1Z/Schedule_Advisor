

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule_advisor', '0002_remove_user_is_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crse_id', models.IntegerField(default=0)),
                ('descr', models.CharField(max_length=300)),
                ('subject', models.CharField(max_length=5)),
                ('class_capacity', models.IntegerField(default=0)),
                ('days', models.CharField(max_length=10)),
                ('class_section', models.IntegerField(default=0)),
            ],
        ),
    ]
