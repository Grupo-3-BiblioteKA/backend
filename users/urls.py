from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("users/", views.UserView.as_view()),
    path("login/", jwt_views.TokenObtainPairView.as_view()),
    path("users/<str:pk>/", views.UserDetailView.as_view()),
    path("users/<str:pk>/loans/", views.UserLoanView.as_view()),
    path("users/<str:pk>/status/", views.UserStatus.as_view()),
    path("users/<str:pk>/follow/", views.UserFollowView.as_view()),
]
