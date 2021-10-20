from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView


@api_view(['GET'])
def home(request):
    context = {
        'Messages': '/api/message',
    }
    return Response(context)
