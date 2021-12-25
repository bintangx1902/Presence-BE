from django.urls import path
from .views import main, controller as con

app_name = 'api'

""" main.py """
urlpatterns = [
    path('', main.home, name='home'),
    path('login', main.UserLoginEndPoint.as_view(), name='api-login'),
    path('auth', main.UserAuthenticated.as_view(), name='api-authenticated'),
    path('logout', main.UserLogoutEndPoint.as_view(), name='api-logout'),
    path('agc', main.AllAgencyNameViews.as_view(), name='agency'),
]

""" controller.py """
urlpatterns += [
    path('agency', con.ControllerMainEndPoint.as_view(), name='controller-api'),
    path('agency/qr', con.QRCodeForPresence.as_view(), name='controller-qr-api'),
]
