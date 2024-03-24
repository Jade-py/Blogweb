from django.urls import path, include
from .views import signup_view, home_view, LoginView, registration_view

urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('signup/register/', registration_view, name='registration'),
]
