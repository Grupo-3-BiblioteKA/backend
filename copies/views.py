from django.shortcuts import render
from .models import Copy
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.permissions import IsCollaborator
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView
from . serializers import CopySerializer


class CopyView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCollaborator]
    queryset = Copy.objects.all()
    serializer_class = CopySerializer


class CopyViewDetail(RetrieveDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCollaborator]
    queryset = Copy.objects.all()
    serializer_class = CopySerializer

    lookup_url_kwarg = "copy_id"


