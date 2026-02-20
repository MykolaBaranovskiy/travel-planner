import logging

from django.db import transaction

from rest_framework import serializers

from .models import Place, TravelProjectPlace, TravelProject

LOGGER = logging.getLogger(__name__)

class TravelProjectPlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = TravelProjectPlace
        fields = ["id", "place", "notes", "visited", "created_at", "updated_at"]
        read_only_fields = ["id", "project"]

class TravelProjectSerializer(serializers.ModelSerializer):
    places = serializers.SerializerMethodField()

    class Meta:
        model = TravelProject
        fields = ["id", "name", "description", "places", "completed", "start_date", "created_at", "updated_at"]
        read_only_fields = ["id", "places", "completed", "created_at", "updated_at"]

    def get_places(self, obj):
        places = TravelProjectPlace.objects.filter(project=obj)
        return TravelProjectPlaceSerializer(places, many=True).data

class TravelProjectCreateSerializer(serializers.ModelSerializer):
    places = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = TravelProject
        fields = ["id", "name", "description", "start_date", "places"]

    def validate_places(self, places_ids):
        if len(places_ids) > 10:
            raise serializers.ValidationError("A project can contain less than 10 places")

        if len(set(places_ids)) != len(places_ids):
            raise serializers.ValidationError("List can't contain duplicates")

        existing_ids = set(
            Place.objects.filter(id__in=places_ids).values_list("id", flat=True)
        )
        missing_ids = set(places_ids) - existing_ids

        if missing_ids:
            raise serializers.ValidationError("Missing place specified")

        return places_ids

    @transaction.atomic
    def create(self, validated_data):
        places_ids = validated_data.pop("places", [])
        user = self.context["request"].user

        project = TravelProject.objects.create(user=user, **validated_data)

        if places_ids:
            places = Place.objects.filter(id__in=places_ids)

            TravelProjectPlace.objects.bulk_create([
                TravelProjectPlace(project=project, place=place)
                for place in places
            ])

        return project
    
class TravelProjectAddPlaceSerializer(serializers.Serializer):
    project = serializers.PrimaryKeyRelatedField(queryset=TravelProject.objects.all())
    place = serializers.PrimaryKeyRelatedField(queryset=Place.objects.all())

    def validate(self, attrs):
        project = attrs.get("project")
        place = attrs.get("place")

        if TravelProjectPlace.objects.filter(project=project, place=place).exists():
            raise serializers.ValidationError("This place is already in the project.")

        current_count = TravelProjectPlace.objects.filter(project=project).count()
        if current_count + 1 > 10:
            raise serializers.ValidationError("A project can contain at most 10 places.")

        return attrs

    def add_place(self):
        project = self.validated_data["project"]
        place = self.validated_data["place"]

        tpp = TravelProjectPlace.objects.create(project=project, place=place)
        return TravelProjectPlaceSerializer(tpp).data
    
class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ["id", "title", "created_at", "updated_at"]
        read_only_fields = fields