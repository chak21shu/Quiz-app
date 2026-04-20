from django.db import models
from quizapp.models import Quiz

class questions(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    question = models.CharField(max_length=500)
    option1 =  models.CharField(max_length=500)
    option2 =  models.CharField(max_length=500)
    option3 =  models.CharField(max_length=500)
    option4 =  models.CharField(max_length=200)
    correct_answer = models.IntegerField()

    
