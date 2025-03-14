from django.db import models

class Contact(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return f"Contact from {self.name}"

    class Meta:
        db_table = 'Contact'