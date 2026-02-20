from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register("register", views.UserRegisterViewSet, basename="register")

urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    path("", include(router.urls)),
]