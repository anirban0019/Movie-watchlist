from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    release_year = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=[("To Watch", "To Watch"), ("Watched", "Watched")],
        default="To Watch"
    )

    def __str__(self):
        return f"{self.title} ({self.release_year}) - {self.status}"
