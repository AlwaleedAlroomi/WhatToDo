from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True, null=True)
    due = models.DateField(blank=True, null=True)
    isCompleted = models.BooleanField(blank=True, null=False, default=False)

    def __str__(self):
        return f'({self.id} {self.user}) {self.title}'
