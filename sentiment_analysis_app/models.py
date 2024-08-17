from django.db import models
from django.contrib.auth.models import User


class Analysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    input_text = models.TextField()
    polarity = models.FloatField()
    subjectivity = models.FloatField()
    analysis_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Analysis {self.id} by {self.user.username if self.user else 'Anonymous'}"
        )
