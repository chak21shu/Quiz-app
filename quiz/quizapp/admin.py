from django.contrib import admin
from .models import Quiz,Attempt,TotalParticipants
from questions.models import questions
from answer_app.models import Answers

admin.site.register(Quiz)
admin.site.register(questions)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['user','quiz','question','selected_option','score']

admin.site.register(Answers,AnswerAdmin)
admin.site.register(Attempt)
admin.site.register(TotalParticipants)

