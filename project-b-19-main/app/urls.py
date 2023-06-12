from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    # path('', lambda request: redirect('home/', permanent=False)),
    path('', include('schedule_advisor.urls')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('logout', LogoutView.as_view()),
]

urlpatterns += staticfiles_urlpatterns()