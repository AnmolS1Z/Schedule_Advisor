# Generated by Django 4.1.7 on 2023-03-18 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule_advisor', '0003_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='N/A', max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days', models.CharField(default='N/A', max_length=100)),
                ('st_time', models.CharField(default='00:00', max_length=10)),
                ('end_time', models.CharField(default='23:59', max_length=10)),
                ('building', models.CharField(default='N/A', max_length=100)),
                ('room', models.CharField(default='N/A', max_length=100)),
                ('st_date', models.CharField(default='N/A', max_length=10)),
                ('end_date', models.CharField(default='N/A', max_length=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='course',
            name='days',
        ),
        migrations.AddField(
            model_name='course',
            name='catalog_number',
            field=models.CharField(default='0000', max_length=10),
        ),
        migrations.AddField(
            model_name='course',
            name='class_nbr',
            field=models.IntegerField(default=0, unique=True),
        ),
        migrations.AddField(
            model_name='course',
            name='enrollment',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='course',
            name='instruction_mode',
            field=models.CharField(default='N/A', max_length=100),
        ),
        migrations.AddField(
            model_name='course',
            name='term',
            field=models.CharField(default='N/A', max_length=300),
        ),
        migrations.AddField(
            model_name='course',
            name='units',
            field=models.IntegerField(default=0),
        ),
        migrations.AddConstraint(
            model_name='course',
            constraint=models.UniqueConstraint(fields=('term', 'class_nbr'), name='schedule_advisor_course_unique'),
        ),
        migrations.AddConstraint(
            model_name='meeting',
            constraint=models.UniqueConstraint(fields=('days', 'st_time', 'end_time', 'building', 'room', 'st_date', 'end_date'), name='schedule_advisor_meeting_unique'),
        ),
        migrations.AddField(
            model_name='course',
            name='instructors',
            field=models.ManyToManyField(to='schedule_advisor.instructor'),
        ),
        migrations.AddField(
            model_name='course',
            name='meeting',
            field=models.ManyToManyField(to='schedule_advisor.meeting'),
        ),
    ]
