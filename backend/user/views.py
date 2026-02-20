from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserProfileSerializer

class UserRegisterViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()

class UserLoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.user_tokens(), status=status.HTTP_200_OK)

class UserProfileView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)