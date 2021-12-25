from .main import *


class ControllerMainEndPoint(APIView):
    # renderer_classes = [JSONRenderer]

    def get(self, format=None):
        token = self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("UnAuthenticated")

        payload = payloads(token)
        user = get_object_or_404(User, id=payload['user_id'])
        serializer = AgencySerializer(user.user.agency, many=False)

        return Response(serializer.data)

    def post(self, format=None):
        return Response()


class QRCodeForPresence(APIView):
    def get(self, format=None):
        token = self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("UnAuthenticated")

        payload = payloads(token)
        user = get_object_or_404(User, id=payload['user_id'])
        qr = QRCodeGenerator.objects.filter(agency=user.user.agency)
        serializer = QRCodeSerializer(qr, many=True)
        return Response(serializer.data)

    def post(self, format=None):

        return Response()
