from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, render, get_object_or_404
from django import forms
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SF
from schedule_advisor.models import Course, Meeting, Instructor, Subject, User, ShoppingCart
import requests, string
from django.urls import reverse
from django.views import generic
from django.contrib import messages


class MyCustomSocialSignupForm(SF):
    is_teacher = forms.BooleanField(required=False, label='Are you a teacher?:')

    def save(self, request):
        user = super(MyCustomSocialSignupForm, self).save(request)
        user.is_teacher = self.cleaned_data['is_teacher']
        user.save()
        # You must return the original result.
        return user


class MyCustomSignupForm(SignupForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    is_teacher = forms.BooleanField(required=False, label='Please check this box if you are a teacher:')

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm, self).save(request)

        # Add your own processing here.
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_teacher = self.cleaned_data['is_teacher']
        user.save()
        # You must return the original result.
        return user


def index(request):
    userList = User.objects.all()
    return render(request, 'schedule_advisor/home.html', {'users': userList})


def login(request):
    return render(request, 'schedule_advisor/login.html')


def schedule(request):
    return render(request, 'schedule_advisor/schedule.html')


def add_course(request, user_id, course_id):
    user = get_object_or_404(User, pk=user_id)
    course_added = get_object_or_404(Course, id=course_id)
    print('DSNDOSd')
    print(user.username)
    print(course_added)
    print('Doing something')
    if course_added not in user.shopping_cart.all():
        print('IF')
        user.shopping_cart.add(course_added)

    if schedule_conflict(user):
        user.shopping_cart.remove(course_added)
        messages.error(request, "Error, "+course_added.descr +" has a Time Conflict with your Current Schedule")
    else:
        user.status = -2
        messages.success(request, "Success, "+course_added.descr +" has been Added to your Cart")
    print(user.shopping_cart.count())
    user.save()
    print('DONE')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_course(request, user_id, course_id):
    user = get_object_or_404(User, pk=user_id)
    course = get_object_or_404(Course, id=course_id)
    # print('DSNDOSd')
    # print(user.username)
    # print(course)
    # print('Doing something')
    if course in user.shopping_cart.all():
        # print('IF')
        user.shopping_cart.remove(course)
        user.status = -2
    # print(user.shopping_cart.count())
    user.save()
    # print('DONE')
    messages.success(request, "Success, "+course.descr +" has been Removed to your Cart")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def get_subjects(request):
    url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01"
    subs = requests.get(url).json()
    Subject.objects.all().delete()
    all_subjects = {}
    for sub in subs['subjects']:
        subject_data = None
        if Subject.objects.filter(name=sub['subject']).exists():
            subject_data = Subject.objects.filter(name=sub['subject'])[0]
        else:
            subject_data = Subject(name=sub['subject'], descr=sub['descr'])
            subject_data.save()
        all_subjects = Subject.objects.all().order_by('name')
    return all_subjects


def get_courses(request):
    # https://dev.to/yahaya_hk/how-to-populate-your-database-with-data-from-an-external-api-in-django-398i

    # Course.objects.all().delete()
    all_courses = {}
    filters = {}
    all_subs = get_subjects(request)
    if 'subject' in request.GET:
        subj = request.GET['subject']
        if subj != '':
            filters['subject'] = subj
    if 'catalog_num' in request.GET:
        cat_num = request.GET['catalog_num']
        if cat_num != '':
            filters['catalog_number'] = cat_num
    if 'instructor' in request.GET:
        inst = request.GET['instructor']
        if inst != '':
            filters['instructors'] = inst
    if 'class_nbr' in request.GET:
        class_nbr = request.GET['class_nbr']
        if class_nbr != '':
            filters['class_nbr'] = class_nbr
    if 'im' in request.GET:
        im = request.GET['im']
        if im != '':
            filters['instruction_mode'] = im
    if 'descr' in request.GET:
        descr = request.GET['descr']
        if descr != '':
            filters['descr'] = descr
    if 'instructors' in filters.keys():
        instr = filters['instructors']
        del filters['instructors']
        all_courses = Course.objects.filter(instructors__name__contains=instr, **filters).order_by('catalog_number')
    elif len(filters.keys()) > 0:
        all_courses = Course.objects.filter(**filters).order_by('catalog_number')
    return render(request, 'schedule_advisor/course.html', {"all_courses": all_courses, "all_subjects": all_subs})


def course_detail(request, id):
    course = Course.objects.get(id=id)
    return render(
        request,
        'schedule_advisor/course_detail.html',
        {'course': course}
    )


def shopping_cart(request):
    return render(request, 'schedule_advisor/shopping_cart.html')


def view_student_cart(request, user_id):
    user = User.objects.get(pk=user_id)
    print(user.username)
    return render(request, 'schedule_advisor/student_cart.html', {'student': user})


def approve(request, user_id):
    print(user_id)
    user = get_object_or_404(User, pk=user_id)
    user.status = 1
    user.message = "Your Schedule has been approved!"
    user.save()
    return HttpResponseRedirect(reverse('schedule_advisor:home'))


def reject(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.status = -1
    user.message = request.GET['rejection']
    user.save()
    return HttpResponseRedirect(reverse('schedule_advisor:home'))


def submit_schedule(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if schedule_conflict(user):
        user.status = -2
        user.message = 'Your schedule is not valid, there is a scheduling conflict.'
        user.save()

    else:
        user.status = 0
        user.message = 'Your schedule has been submitted to your advisor! \nAwaiting approval...'
        user.save()
    return HttpResponseRedirect(reverse('schedule_advisor:home'))

def schedule_conflict(user):
    for course in user.shopping_cart.all():
        for comparing_course in user.shopping_cart.all():
            for course_meeting in course.meeting.all():
                for comparing_course_meeting in comparing_course.meeting.all():
                    if course.class_nbr != comparing_course.class_nbr:
                        if len(course_meeting.days) != 0 and len(comparing_course_meeting.days) !=0:
                            if ('Mo' in course_meeting.days and 'Mo' in comparing_course_meeting.days) or ('Tu' in course_meeting.days and 'Tu' in comparing_course_meeting.days) or('We' in course_meeting.days and 'We' in comparing_course_meeting.days) or('Th' in course_meeting.days and 'Th' in comparing_course_meeting.days) or('Fr' in course_meeting.days and 'Fr' in comparing_course_meeting.days):
                                first_course_starting_time = Convert_Time_String_into_Int(course_meeting.st_time)
                                first_course_ending_time = Convert_Time_String_into_Int(course_meeting.end_time)
                                second_course_starting_time = Convert_Time_String_into_Int(comparing_course_meeting.st_time)
                                second_course_ending_time = Convert_Time_String_into_Int(comparing_course_meeting.end_time)

                                if (first_course_starting_time >= second_course_starting_time and first_course_starting_time <= second_course_ending_time):
                                    return True
                                if (second_course_starting_time>= first_course_starting_time and second_course_starting_time <= first_course_ending_time):
                                    return True

    return False


def Convert_Time_String_into_Int(meeting_time):
    return 100 * ((int)(meeting_time[0:2])) + ((int)(meeting_time[3:5]))

