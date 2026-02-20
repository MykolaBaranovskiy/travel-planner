from django.db import models

from user.models import User

from .mixins import ModelMixin

class Place(ModelMixin):
    id = models.IntegerField(primary_key=True, unique=True)
    title = models.CharField(max_length=255)

class UserPlace(ModelMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)
    visited = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "place"], name="unique_user_place")
        ]

class TravelProject(ModelMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    places = models.ManyToManyField(UserPlace)
    completed = models.BooleanField(default=False)