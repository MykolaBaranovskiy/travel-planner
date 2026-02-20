from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import User
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserProfileSerializer

class UserRegisterViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()

    @swagger_auto_schema(
        operation_summary="Register User",
        operation_description="Register User",
        responses={
            200: UserRegisterSerializer,
            401: "Unauthorized - Invalid or missing token",
        },
        request_body=UserRegisterSerializer,
        tags=["User"],
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="JWT token with Bearer prefix (Bearer <token>)",
                type=openapi.TYPE_STRING,
                required=True,
                example="Bearer your_jwt_token_here",
            )
        ],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class UserLoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    @swagger_auto_schema(
        operation_summary="Login User",
        operation_description="Login User",
        responses={
            200: UserLoginSerializer,
            401: "Unauthorized - Invalid or missing token",
        },
        request_body=UserLoginSerializer,
        tags=["User"],
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="JWT token with Bearer prefix (Bearer <token>)",
                type=openapi.TYPE_STRING,
                required=True,
                example="Bearer your_jwt_token_here",
            )
        ],
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.user_tokens(), status=status.HTTP_200_OK)

class UserProfileView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    @swagger_auto_schema(
        operation_summary="User Profile",
        operation_description="User Profile",
        responses={
            200: UserProfileSerializer,
            401: "Unauthorized - Invalid or missing token",
        },
        request_body=UserProfileSerializer,
        tags=["User"],
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="JWT token with Bearer prefix (Bearer <token>)",
                type=openapi.TYPE_STRING,
                required=True,
                example="Bearer your_jwt_token_here",
            )
        ],
    )
    def get(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)