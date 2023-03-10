from django.shortcuts import render
from .models import User
from copies.models import Loans
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView
from .permissions import IsAccountOwner, IsCollaborator
from .serializer import UserSerializer
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
        return Loans.objects.filter(user_id=self.kwargs.get("pk"))
