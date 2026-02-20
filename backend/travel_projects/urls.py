from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register("travel_project", views.TravelProjectViewSet, basename="travel-project-list")
router.register("travel_project_place", views.TravelProjectPlaceViewSet, basename="travel-project-place-edit")
router.register("place", views.PlaceViewSet, basename="place")

urlpatterns = [
    path("add_place/", views.TravelProjectAddPlaceView.as_view(), name="add-place"),
    path("", include(router.urls))
]
