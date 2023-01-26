from django.urls import path

from user_profile.views import Login

urlpatterns = [
    path('login/', Login.as_view()),
]
