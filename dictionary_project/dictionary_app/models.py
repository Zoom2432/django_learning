from django.db import models
from django.contrib.auth.models import User

class Dict(models.Model):
    word = models.CharField(max_length=100)
    translation = models.CharField(max_length=250)
    prompt = models.CharField(max_length=250, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.word
