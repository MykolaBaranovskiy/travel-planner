from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import TravelProject, Place, TravelProjectPlace

from .serializers import (
    TravelProjectSerializer,
    TravelProjectCreateSerializer,
    TravelProjectAddPlaceSerializer,
    TravelProjectPlaceSerializer,
    PlaceSerializer,
)

class TravelProjectViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TravelProject.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return TravelProjectCreateSerializer
        return TravelProjectSerializer
    
    def perform_destroy(self, instance):
        if TravelProjectPlace.objects.filter(project=instance, visited=True).exists():
            raise ValidationError("You can't delete a project with visited places.")
        
        instance.delete()

    @swagger_auto_schema(
        operation_summary="List Travel Project",
        operation_description="List travel project",
        responses={
            200: TravelProjectSerializer,
            401: "Unauthorized - Invalid or missing token",
        },
        tags=["TravelProject"],
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
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Create Travel Project",
        operation_description="Create travel project",
        request_body=TravelProjectCreateSerializer,
        responses={
            201: TravelProjectCreateSerializer,
            401: "Unauthorized - Invalid or missing token",
        },
        tags=["TravelProject"],
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
    
    @swagger_auto_schema(
        operation_summary="Retrieve Travel Project",
        operation_description="Retreive travel project",
        responses={
            200: TravelProjectSerializer,
            401: "Unauthorized - Invalid or missing token",
        },
        tags=["TravelProject"],
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
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Update Travel Project",
        operation_description="Update travel project",
        responses={
            200: TravelProjectSerializer,
            401: "Unauthorized - Invalid or missing token",
        },
        request_body=TravelProjectCreateSerializer,
        tags=["TravelProject"],
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
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Destroy Travel Project",
        operation_description="Destroy travel project",
        responses={
            204: TravelProjectSerializer,
            401: "Unauthorized - Invalid or missing token",
        },
        tags=["TravelProject"],
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
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class TravelProjectAddPlaceView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TravelProjectAddPlaceSerializer

    @swagger_auto_schema(
        operation_summary="Add Place To Travel Project",
        operation_description="Add Place To Travel Project",
        responses={
            201: TravelProjectAddPlaceSerializer,
            401: "Unauthorized - Invalid or missing token",
        },
        request_body=TravelProjectAddPlaceSerializer,
        tags=["TravelProject"],
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
        result = serializer.add_place()
        return Response(result, status=status.HTTP_201_CREATED)
    
class TravelProjectPlaceViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TravelProjectPlaceSerializer

    @swagger_auto_schema(
        operation_summary="Retrieve Travel Project Place",
        operation_description="Retrieve Travel Project Place",
        responses={
            200: TravelProjectPlaceSerializer,
            401: "Unauthorized - Invalid or missing token",
        },
        tags=["TravelProject"],
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
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Update Travel Project Place",
        operation_description="Update Travel Project Place",
        responses={
            200: TravelProjectPlaceSerializer,
            401: "Unauthorized - Invalid or missing token",
        },
        request_body=TravelProjectPlaceSerializer,
        tags=["TravelProject"],
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
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    def get_queryset(self):
        return TravelProjectPlace.objects.filter(project__user=self.request.user)
    
class PlaceViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PlaceSerializer
    queryset = Place.objects.all()

    @swagger_auto_schema(
        operation_summary="List Places",
        operation_description="List Places",
        responses={
            200: PlaceSerializer,
            401: "Unauthorized - Invalid or missing token",
        },
        tags=["TravelProject"],
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
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)