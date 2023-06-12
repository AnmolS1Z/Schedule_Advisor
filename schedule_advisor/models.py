# from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser


class Instructor(models.Model):
    name = models.CharField(max_length=100, default='N/A')
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Meeting(models.Model):
    days = models.CharField(max_length=100, default='N/A')
    st_time = models.CharField(max_length=10, default='N/A')
    end_time = models.CharField(max_length=10, default='N/A')
    building = models.CharField(max_length=100, default='N/A')
    room = models.CharField(max_length=100, default='N/A')
    st_date = models.CharField(max_length=10, default='N/A')
    end_date = models.CharField(max_length=10, default='N/A')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['days', 'st_time', 'end_time', 'building', 'room', 'st_date', 'end_date'],
                                    name="%(app_label)s_%(class)s_unique")
        ]

    def __str__(self):
        return f'{self.days}, {self.st_time}-{self.end_time}, {self.building} {self.room}'


class Course(models.Model):
    crse_id = models.IntegerField(default=0)
    descr = models.CharField(max_length=300)
    subject = models.CharField(max_length=5)
    class_capacity = models.IntegerField(default=0)
    meeting = models.ManyToManyField(Meeting)
    class_section = models.CharField(default='', max_length=20)  # test comment
    class_nbr = models.CharField(default='00000', max_length=10)
    instructors = models.ManyToManyField(Instructor)
    units = models.CharField(default='0', max_length=10)
    term = models.CharField(max_length=300, default='N/A')
    # times = models.CharField(max_length=300, default='N/A')
    instruction_mode = models.CharField(max_length=100, default='N/A')
    enrollment = models.IntegerField(default=0)
    catalog_number = models.CharField(max_length=10, default='0000')
    section_type = models.CharField(max_length=10, default='Lecture')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['term', 'class_nbr', 'subject', 'catalog_number'],
                                    name="%(app_label)s_%(class)s_unique")
        ]

    def __str__(self):
        return self.descr  # Will need to change this eventually but should be fine for now


class ShoppingCart(models.Model):
    courses = models.ManyToManyField(Course)


# Create your models here.
class User(AbstractUser):
    # we can just have 1 boolean, I think just 1 is fine. True for teacher, false for student
    # is_student = models.BooleanField('student status', default=False)
    is_teacher = models.BooleanField('teacher status', default=False)
    shopping_cart = models.ManyToManyField(Course)
    status = models.IntegerField(default=-2)
    message = models.CharField(max_length=5000, default='')



class Subject(models.Model):
    name = models.CharField(max_length=10, unique=True)
    descr = models.CharField(max_length=100, default='N/A')

    def __str__(self):
        return self.name
