import datetime, jwt
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from ..serializers import *
from ..utils import *
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.decorators import renderer_classes
from django.utils import timezone


def payloads(token):
    try:
        payload = jwt.decode(token, 'secret', algorithms='HS256')
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("UnAuthenticated!")

    return payload


def this_user(payload):
    return get_object_or_404(User, id=payload['user_id'])


@api_view(['GET'])
def home(request):
    return render(request, 'api/main.html')


class AllAgencyNameViews(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, format=None):
        agency = AgencyName.objects.all()
        serializer = AgencySerializer(agency, many=True)
        return Response(serializer.data)


class UserLoginEndPoint(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, format=None):
        token = self.request.COOKIES.get('jwt')
        if token:
            response = Response()
            response.data = {
                'jwt': token
            }
            return response
        return Response(status.HTTP_204_NO_CONTENT)

    def post(self, format=None):
        username = self.request.data['username']
        password = self.request.data['password']
        user = User.objects.filter(username=username).first()
        if not user:
            raise AuthenticationFailed("User Not Found")
        user = UserExtended.objects.filter(user=user).first()
        if not user:
            raise AuthenticationFailed("User is not registered")
        user = get_object_or_404(User, username=username)
        if not user.check_password(password):
            raise AuthenticationFailed("Wrong Password!")

        payload = {
            'user_id': user.id,
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token)
        response.data = {
            'jwt': token
        }

        return response


class UserAuthenticated(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, format=None):
        token = self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("UnAuthenticated")

        payload = payloads(token)
        user = this_user(payload)
        user_serializer = UserSerializer(user, many=False)
        extend_serializer = UserExtendedSerializer(user.user, many=False)
        agency_serializer = AgencySerializer(user.user.agency, many=False)

        return Response({
            "user": user_serializer.data,
            'extended': extend_serializer.data,
            "agency": agency_serializer.data
        })


class UserLogoutEndPoint(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, format=None):
        token = self.request.COOKIES.get('jwt')
        if token:
            response = Response()
            response.data = {
                'jwt': token
            }
            return response
        return Response(status.HTTP_204_NO_CONTENT)

    def post(self, format=None):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'messages': "Success!",
            'status': status.HTTP_204_NO_CONTENT
        }
        return response
