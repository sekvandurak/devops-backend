from django.db import models
from django.utils import timezone

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # No default needed

    def __str__(self):
        return self.question