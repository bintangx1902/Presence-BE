from django.urls import path
from .views import presence as p, controller as c, main

app_name = 'dash'

''' this url patterns for main purpose '''
urlpatterns = [
    path('', main.redirection, name='main'),
    path('register', main.account_register, name='manual'),
    path('agency/create', main.CreateAgency.as_view(), name='agency'),
    path('invitation-forms/<slug:link>', main.register_by_invitation, name='invitation'),
    path('landed/', main.LandingPage.as_view(), name='landing'),
]

''' this url patterns for controller only '''
urlpatterns += [
    path('<link>/registering-employee', c.registering_user, name='registering-user'),
    path('<link>/generate-presence-qr', c.CreateQRCode.as_view(), name='create-qr'),
    path('<link>', c.DashboardView.as_view(), name='agency-dashboard'),
]

''' this url patterns for presence only '''
urlpatterns += [

]
