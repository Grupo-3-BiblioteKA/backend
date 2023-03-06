from django.shortcuts import render
from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .permissions import IsAccountOwner, IsCollaborator
from .serializer import UserSerializer


class UserView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCollaborator]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]

    queryset = User.objects.all()
    serializer_class = UserSerializer
