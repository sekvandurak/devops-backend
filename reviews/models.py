
from django.db import models
from users.models import Users

class Reviews(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    body = models.TextField()
    stars = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user.name} - {self.stars} stars"

    class Meta:
        db_table = 'Reviews'