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
        unique = self.request.GET.get('unique')
        token = self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("UnAuthenticated! ", status.HTTP_403_FORBIDDEN)

        if not unique:
            raise AuthenticationFailed("Agency Code not found", status.HTTP_403_FORBIDDEN)

        agency = AgencyName.objects.filter(unique_code=unique)
        if not agency:
            raise AuthenticationFailed("Agency is not registered! ", status.HTTP_403_FORBIDDEN)
        agency = get_object_or_404(AgencyName, unique_code=unique)

        payload = payloads(token)
        user = this_user(payload)
        qr = get_object_or_404(QRCodeGenerator, qr_code=self.request.data['code'])

        if qr.qr_code != user.user.agency:
            raise AuthenticationFailed("Your Agency is not same like the QR code", status.HTTP_404_NOT_FOUND)

        recap = PresenceRecap.objects.create(
            qr=qr, user=user.user
        )
        recap.save()

        history = PresenceRecap.objects.filter(user=user.user)
        serializer = PresenceRecapSerializer(history, many=True)
        return Response(serializer.data)


class UserHistoryDetail(APIView):
    def get(self, format=None):
        return Response()
