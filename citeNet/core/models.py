from django.db import models
from django.contrib.auth.models import User

class History(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    history = models.JSONField(default=dict)  # JSONField to store the data
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']