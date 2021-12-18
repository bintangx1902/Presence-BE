from django.urls import path
from .views import main

app_name = 'api'

urlpatterns = [
    path('', main.home, name='home'),
    path('login', main.UserLoginEndPoint.as_view(), name='api-login'),
    path('auth', main.UserAuthenticated.as_view(), name='api-authenticated'),
    path('logout', main.UserLogoutEndPoint.as_view(), name='api-logout'),
    path('agc', main.AllAgencyNameViews.as_view(), name='agency'),
]

