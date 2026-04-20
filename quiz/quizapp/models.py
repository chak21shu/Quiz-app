from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
   
    title = models.CharField(max_length=400)
    description = models.CharField(max_length=1000)
    totalquestions = models.IntegerField()
    time = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True, blank=True)
    
    

 

class Attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField()
    taken_at = models.DateTimeField(auto_now_add=True)


class TotalParticipants(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_participants = models.IntegerField(default=0)