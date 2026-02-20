from django.db import models

from user.models import User

from .mixins import ModelMixin

class Place(ModelMixin):
    id = models.IntegerField(primary_key=True, unique=True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title}"

class TravelProject(ModelMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.start_date}"
    
class TravelProjectPlace(ModelMixin):
    project = models.ForeignKey(TravelProject, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)
    visited = models.BooleanField(default=False)

    class Meta:
        unique_together = ("project", "place")

    def __str__(self):
        return f"{self.project.name} - {self.place.title}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._update_project_completed()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self._update_project_completed()

    def _update_project_completed(self):
        project = self.project
        all_visited = not project.travelprojectplace_set.filter(visited=False).exists()
        if project.completed != all_visited:
            project.completed = all_visited
            project.save(update_fields=["completed"])