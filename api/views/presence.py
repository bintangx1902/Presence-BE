from .main import *
from rest_framework import serializers


class UserPresenceHIstory(APIView):
    def get(self, format=None):
        token = self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("UnAuthenticated! ", status.HTTP_403_FORBIDDEN)
        payload = payloads(token)
        user = this_user(payload)

        history = PresenceRecap.objects.filter(user=user.user)
        serializer = PresenceRecapSerializer(history, many=True)
        return Response(serializer.data)

    def post(self, format=None):
        return
