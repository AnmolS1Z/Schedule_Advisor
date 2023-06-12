from django.urls import path, include

from . import views

app_name = 'schedule_advisor'
urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login, name='login'),
    path('courses/', views.get_courses, name="courses"),
    path('courses/<int:id>/', views.course_detail, name="course_detail"),
    path('schedule/', views.schedule, name='schedule'),
    path('<int:user_id>/<int:course_id>/add/', views.add_course, name='add_course'),
    path('<int:user_id>/<int:course_id>/drop/', views.remove_course, name='remove_course'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
    path('<int:user_id>/cart_view/', views.view_student_cart, name='student_cart'),
    path('<int:user_id>/approved/', views.approve, name='approval'),
    path('<int:user_id>/rejected/', views.reject, name='rejection'),
    path('<int:user_id>/submit/', views.submit_schedule, name='submit_schedule')
]
# path('home/', views.index, name='home'),
