from django.urls import path
from .views import presence as p, controller as c, main

app_name = 'dash'

urlpatterns = [
    path('', main.redirection, name='main'),
    path('manual-registering', main.manual_registration, name='manual'),
    path('account/register', main.account_register, name='std'),
    path('agency/create', main.CreateAgency.as_view(), name='agency'),
    path('invitation-forms/<slug:link>', main.register_by_invitation, name='invitation'),
    path('landed', main.LandingPage.as_view(), name='landing')
]

urlpatterns += [
    path('<link>/registering-employee', c.registering_user, name='registering-user'),
]

urlpatterns += [

]
