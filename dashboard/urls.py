from django.urls import path
from .views import presence as p, supervisor as s, main

app_name = 'dash'

urlpatterns = [
    path('', main.main, name='main'),
    path('<link>/registering-employee', s.registering_user, name='registering-user')
]
