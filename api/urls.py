from django.urls import path
from .views import main, controller as con, presence as pre

app_name = 'api'

""" main.py """
urlpatterns = [
    path('', main.home, name='home'),
    path('login', main.UserLoginEndPoint.as_view(), name='api-login'),
    path('auth', main.UserAuthenticated.as_view(), name='api-authenticated'),
    path('logout', main.UserLogoutEndPoint.as_view(), name='api-logout'),
    path('agc', main.AllAgencyNameViews.as_view(), name='agency'),
]


""" presence.py """
urlpatterns += [
    path('agency/user/history', pre.UserPresenceHIstory.as_view(), name='api-user-history'),
    path('agency/user/history-detail', pre.UserHistoryDetail.as_view(), name='api-user-history-detail'),
]


""" controller.py """
urlpatterns += [
    path('agency/qr', con.QRCodeForPresence.as_view(), name='controller-qr-api'),
    path('agency/inv', con.InvitationLinkEndPoint.as_view(), name='invitation-link-api'),
    path('agency', con.ControllerMainEndPoint.as_view(), name='controller-api'),
]
