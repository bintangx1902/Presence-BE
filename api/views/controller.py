import datetime

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


class QRCodeForPresence(APIView):
    def get(self, format=None):
        token = self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("UnAuthenticated")

        payload = payloads(token)
        user = this_user(payload)
        qr = QRCodeGenerator.objects.filter(agency=user.user.agency, valid_until__gte=timezone.now())
        serializer = QRCodeSerializer(qr, many=True)
        return Response(serializer.data)

    def post(self, format=None):
        token = self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("UnAuthenticated")

        unique = self.request.GET.get('unique')
        if not unique:
            raise AuthenticationFailed("There is no Agency Code! ", status.HTTP_403_FORBIDDEN)
        agency = AgencyName.objects.filter(unique_code=unique)
        if not agency:
            raise AuthenticationFailed("Broken Code", status.HTTP_403_FORBIDDEN)

        payload = payloads(token)
        user = this_user(payload)
        valid_until = timezone.now() + datetime.timedelta(.5)
        all_qr = QRCodeGenerator.objects.all()
        qrs = [x.qr_code for x in all_qr]
        code = generate_qr_code()
        while True:
            if code in qrs:
                code = generate_qr_code()
            else:
                break

        QRCodeGenerator.objects.create(
            qr_code=code, valid_until=valid_until,
            agency=user.user.agency, creator=user
        )
        qr = QRCodeGenerator.objects.filter(agency=user.user.agency, valid_until__gte=timezone.now())
        serializer = QRCodeSerializer(qr, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class InvitationLinkEndPoint(APIView):
    def get(self, format=None):
        token = self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("UnAuthenticated! ", status.HTTP_403_FORBIDDEN)

        payload = payloads(token)
        user = this_user(payload)
        inv = InvitationLink.objects.filter(agency=user.user.agency, valid_until__gte=timezone.now())
        serializer = InvitationLinkSerializer(inv, many=True)
        return Response(serializer.data)

    def post(self, format=None):
        token = self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("There is no Agency Code! ", status.HTTP_403_FORBIDDEN)
        unique = self.request.GET.get('unique')
        if not unique:
            raise AuthenticationFailed("Agency code not detected!", status.HTTP_403_FORBIDDEN)
        agency = AgencyName.objects.filter(unique_code=unique)
        if not agency:
            raise AuthenticationFailed("There is no such Agency! ", status.HTTP_403_FORBIDDEN)

        payload = payloads(token)
        user = this_user(payload)
        code = generate_invitation_code()
        inv = InvitationLink.objects.all()
        data = [x.link for x in inv]
        valid_until = timezone.now() + datetime.timedelta(.5)
        while True:
            if code in data:
                code = generate_qr_code()
            else:
                break

        InvitationLink.objects.create(
            link=code, valid_until=valid_until,
            agency=user.user.agency, invitee=user
        )

        inv = inv.filter(agency=user.user.agency, valid_until__gte=timezone.now())
        serializer = InvitationLinkSerializer(inv, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
