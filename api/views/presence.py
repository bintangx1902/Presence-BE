from .main import *
from rest_framework import serializers


class UserPresenceHIstory(APIView):
    renderer_classes = [JSONRenderer]

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

        payload = payloads(token)
        user = this_user(payload)
        qr = get_object_or_404(QRCodeGenerator, qr_code=self.request.data['code'])

        if qr.agency != user.user.agency:
            raise AuthenticationFailed("Your Agency is not same like the QR code", status.HTTP_404_NOT_FOUND)

        recap = PresenceRecap.objects.create(
            qr=qr, user=user.user
        )
        recap.save()

        history = PresenceRecap.objects.filter(user=user.user)
        serializer = PresenceRecapSerializer(history, many=True)
        return Response(serializer.data)


class UserHistoryDetail(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, format=None):
        token = self.request.COOKIES.get('jwt')
        recap_id = self.request.GET.get('id')
        if not token:
            raise AuthenticationFailed("UnAuthenticated! ", status.HTTP_403_FORBIDDEN)

        if not recap_id:
            raise AuthenticationFailed("The ID is not detected on system! ", status.HTTP_404_NOT_FOUND)

        payload = payloads(token)
        user = this_user(payload)

        recap = PresenceRecap.objects.filter(id=recap_id, user=user.user)
        if not recap:
            raise AuthenticationFailed("The ID is other presence! ", status.HTTP_204_NO_CONTENT)

        recap = get_object_or_404(PresenceRecap, id=recap_id, user=user.user)
        presence_serializer = PresenceRecapSerializer(recap, many=False)
        qr_serializer = QRCodeSerializer(recap.qr, many=False)

        response = Response()
        response.data = {
            'presence': presence_serializer.data,
            'QR_code': qr_serializer.data
        }
        return response


