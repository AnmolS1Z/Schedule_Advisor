from django.test import TestCase
from .models import User, Course, Instructor, Meeting
from django.urls import reverse


# Create your tests here.
class HomeScreenTest(TestCase):

    def test_login_Student(self):
        """

        """
        self.user = User.objects.create_user(is_teacher=False, username="eep8uv", password='12345')
        login = self.client.login(is_teacher=False, username="eep8uv", password='12345')
        url = reverse('schedule_advisor:home')
        response = self.client.get(url)
        self.assertContains(response, 'Welcome, Student eep8uv')
        self.assertContains(response, 'Home')
        self.assertContains(response, 'Courses')
        self.assertContains(response, 'Shopping Cart')
        self.assertContains(response, 'My Schedule')



    def test_teacher_login_no_students(self):
        self.user = User.objects.create_user(is_teacher=True, username="eep8uv", password='12345')
        login = self.client.login(is_teacher=True, username="eep8uv", password='12345')
        url = reverse('schedule_advisor:home')
        response = self.client.get(url)
        self.assertContains(response, 'Welcome, Teacher eep8uv')
        self.assertContains(response,'View Student Shopping Carts')
        self.assertContains(response, 'Home')
        self.assertContains(response, 'Courses')
        self.assertNotContains(response, 'My Schedule')

    def test_login_Teacher(self):
        """

        """
        self.user = User.objects.create_user(is_teacher=True, username="eep8uv", password='12345')
        login = self.client.login(is_teacher=True, username="eep8uv", password='12345')
        student1 = User.objects.create_user(is_teacher=False, username='gan3dz', password='00000')
        student2 = User.objects.create_user(is_teacher=False, username='Anmol', password='10101')
        student2.status = 1
        student2.save()
        url = reverse('schedule_advisor:home')
        response = self.client.get(url)
        self.assertContains(response, 'Welcome, Teacher eep8uv')
#        self.assertContains(response, 'Undetermined')
        self.assertContains(response, 'Approved')
        self.assertNotContains(response, 'gan3dz')
        self.assertContains(response, 'Anmol')


    def test_home_screen_before_login(self):
        url = reverse('schedule_advisor:home')
        response = self.client.get(url)
        self.assertNotContains(response, 'Welcome, Student')
        self.assertNotContains(response, 'Welcome, Teacher')


class ShoppingCartTest(TestCase):

    def test_shopping_cart_before_login(self):
        url = reverse('schedule_advisor:shopping_cart')
        response = self.client.get(url)
        self.assertContains(response, 'Login')
        self.assertNotContains(response, 'Submit')

    def test_shopping_cart_teacher(self):
        self.user = User.objects.create_user(is_teacher=True, username="eep8uv", password='12345')
        login = self.client.login(is_teacher=True, username="eep8uv", password='12345')
        url = reverse('schedule_advisor:shopping_cart')
        response = self.client.get(url)
        self.assertContains(response, "Go to")
        self.assertContains(response, "Home")
        self.assertContains(response, "page to view students' shopping carts")

    def test_shopping_cart_student(self):
        self.user = User.objects.create_user(is_teacher=False, username="eep8uv", password='12345')
        login = self.client.login(is_teacher=False, username="eep8uv", password='12345')
        self.course = Course.objects.create(
            descr="Advanced Software Development Techniques",
            catalog_number="3240",
            subject="CS"
        )
        self.user.shopping_cart.add(self.course)
        url = reverse('schedule_advisor:shopping_cart')
        response = self.client.get(url)
        self.assertContains(response, "Submit")
        self.assertContains(response, "CS 3240")
        self.assertContains(response, "Advanced Software Development Techniques")

    def test_shopping_cart_view_teacher(self):
        """

        """
        self.user = User.objects.create_user(is_teacher=True, username="eep8uv", password='12345')
        login = self.client.login(is_teacher=True, username="eep8uv", password='12345')
        student1 = User.objects.create_user(is_teacher=False, username='gan3dz', password='00000')
        self.course = Course.objects.create(
            descr="Advanced Software Development Techniques",
            catalog_number="3240",
            subject="CS"
        )
        student1.shopping_cart.add(self.course)
        student1.save()
        url = reverse('schedule_advisor:student_cart', args=(student1.id,))
        response = self.client.get(url)
        self.assertContains(response, 'Approve')
        self.assertContains(response, 'Reject')
        self.assertContains(response, "CS 3240")
        self.assertContains(response, "Advanced Software Development Techniques")


class CourseTest(TestCase):

    def test_course_detail_empty(self):
        self.course = Course.objects.create(
            descr="Advanced Software Development Techniques",
            catalog_number="3240",
            subject="CS"
        )
        url = reverse('schedule_advisor:course_detail', args=(self.course.id,))
        response = self.client.get(url)
        self.assertContains(response, "CS 3240")
        self.assertContains(response, "Advanced Software Development Techniques")
        self.assertNotContains(response, "Add Class")
        self.assertNotContains(response, "Remove Class")

    def test_course_detail_cart_in(self):
        self.user = User.objects.create_user(is_teacher=False, username="eep8uv", password='12345')
        login = self.client.login(is_teacher=False, username="eep8uv", password='12345')
        self.course = Course.objects.create(
            descr="Advanced Software Development Techniques",
            catalog_number="3240",
            subject="CS"
        )
        self.user.shopping_cart.add(self.course)
        url = reverse('schedule_advisor:course_detail', args=(self.course.id,))
        response = self.client.get(url)
        self.assertContains(response, "CS 3240")
        self.assertContains(response, "Advanced Software Development Techniques")
        self.assertNotContains(response, "Add Class")
        self.assertContains(response, "Remove Class")

    def test_course_detail_cart_out(self):
        self.user = User.objects.create_user(is_teacher=False, username="eep8uv", password='12345')
        login = self.client.login(is_teacher=False, username="eep8uv", password='12345')
        self.course = Course.objects.create(
            descr="Advanced Software Development Techniques",
            catalog_number="3240",
            subject="CS"
        )
        url = reverse('schedule_advisor:course_detail', args=(self.course.id,))
        response = self.client.get(url)
        self.assertContains(response, "CS 3240")
        self.assertContains(response, "Advanced Software Development Techniques")
        self.assertContains(response, "Add Class")
        self.assertNotContains(response, "Remove Class")

class Schedule_Test(TestCase):
    def test_course_in_shopping_cart(self):
        self.user = User.objects.create_user(is_teacher=False, username="eep8uv", password='12345')
        login = self.client.login(is_teacher=False, username="eep8uv", password='12345')
        self.meeting = Meeting.objects.create(
            days='MoWe',
            st_time = '12:30',
            end_time = '13:45'
        )
        self.course = Course.objects.create(
            descr="Advanced Software Development Techniques",
            catalog_number="3240",
            subject="CS",
        )
        self.course.meeting.add(self.meeting)
        self.user.shopping_cart.add(self.course)
        url = reverse('schedule_advisor:schedule')
        response = self.client.get(url)
        self.assertContains(response, "CS 3240")
        self.assertNotContains(response, "APMA 3100")
        self.assertContains(response, "Monday")
        self.assertContains(response, "Tuesday")
        self.assertContains(response, "Wednesday")
        self.assertContains(response, "Thursday")
        self.assertContains(response, "Friday")
        self.assertContains(response, "12:00 PM")

    def test_no_course_in_shopping_cart(self):
        self.user = User.objects.create_user(is_teacher=False, username="eep8uv", password='12345')
        login = self.client.login(is_teacher=False, username="eep8uv", password='12345')
        url = reverse('schedule_advisor:schedule')
        response = self.client.get(url)
        self.assertNotContains(response, "CS 3240")
        self.assertNotContains(response, "APMA 3100")
