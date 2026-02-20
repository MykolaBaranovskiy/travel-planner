from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

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

class TravelProjectAddPlaceView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TravelProjectAddPlaceSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.add_place()
        return Response(result, status=status.HTTP_201_CREATED)
    
class TravelProjectPlaceViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TravelProjectPlaceSerializer
    
    def get_queryset(self):
        return TravelProjectPlace.objects.filter(project__user=self.request.user)
    
class PlaceViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PlaceSerializer
    queryset = Place.objects.all()