from django.db import models

class Features(models.Model):
    header = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.header

    class Meta:
        db_table = 'Features'