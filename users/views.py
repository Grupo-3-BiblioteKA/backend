from django.shortcuts import render
from .models import User
from copies.models import Loans
from books.models import Follow
from books.serializers import FollowSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from .permissions import IsAccountOwner, IsCollaborator
from .serializer import UserSerializer, UserSerializerStatus
from copies.serializers import LoanSerializer
from django.shortcuts import get_object_or_404


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


class UserLoanView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]
    serializer_class = LoanSerializer

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs.get("pk"))
        return Loans.objects.filter(user_id=user.id)


class UserStatus(RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCollaborator]
    queryset = User.objects.all()
    serializer_class = UserSerializerStatus


class UserFollowView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]
    serializer_class = FollowSerializer

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs.get("pk"))
        return Follow.objects.filter(user=user.id)
