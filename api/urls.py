from django.urls import path
from .views import *

app_name = 'api'

urlpatterns = [
    path('', home, name='home'),
]


class MessageEndPoint(APIView):
    def get(self):
        pass
