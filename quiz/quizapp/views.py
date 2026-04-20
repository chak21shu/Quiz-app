from django.shortcuts import render,redirect,get_object_or_404
from quizapp.models import Quiz,Attempt,TotalParticipants
from questions.models import questions
from answer_app.models import Answers
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Avg




def dashboard_view(request):
    user = request.user
    # quizzes = Quiz.objects.filter(created_by=request.user)
    # quizzes_created_by_user = quizzes.count()
    quizzes = Quiz.objects.filter(created_by = user)
    quizzes_created_by_user = len(quizzes)
    total_correct = 0
    total_answers = 0
    for quiz in quizzes:
        score = len(Answers.objects.filter(quiz = quiz, score = 1))
        answers = len(Answers.objects.filter(quiz = quiz))
        total_correct += score
        total_answers += answers
    average = (total_correct / max(total_answers,1)) * 100
    # total_average = 0
    # for quiz in quizzes:
    #     total_attempts = len(Attempt.objects.filter(quiz = quiz))
    #     total_answer = len(Answers.objects.filter(quiz = quiz,score = 1))
    #     total_questions = quiz.totalquestions
    #     Average = total_answer/max((total_attempts*total_questions),1)
    #     total_average += Average
    # Average = total_average/len(quizzes)
    total_attempts = 0
    if TotalParticipants.objects.filter(user=request.user).exists():
        total_attempts = TotalParticipants.objects.filter(user=request.user).first().total_participants
    if request.method == "POST" and request.POST.get("action") == "copy":
        quiz_id = request.POST.get("quiz_to_copy")
        if quiz_id:
            try:
                original = Quiz.objects.get(id=quiz_id, created_by=request.user)
                Quiz.objects.create(
                    created_by=request.user,
                    quiztitle=original.quiztitle + " (Copy)",
                    description=original.description,
                    totalquestions=original.totalquestions
                )
                # You can add question/answer copying logic here
            except Quiz.DoesNotExist:
                pass
            return redirect('dashboard')
    return render(request, 'dashboard.html', {
        'quiz_count': quizzes_created_by_user,
        'total_attempts': total_attempts,
        'quizzes': quizzes,
        'average':average,
    })



def quizform_view(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        totalquestions = int(request.POST['totalquestions'])
        time = request.POST['time']

        quiz_getter = Quiz.objects.create(
            created_by=request.user,
            title=title,
            description=description,
            totalquestions=totalquestions,
            time=time
        )

        for i in range(1, totalquestions + 1):
            question = request.POST[f'question{i}']
            option1 = request.POST[f'q{i}-opt1']
            option2 = request.POST[f'q{i}-opt2']
            option3 = request.POST[f'q{i}-opt3']
            option4 = request.POST[f'q{i}-opt4']
            correct_answer = request.POST[f'q{i}-answer']

            questions.objects.create(
                quiz=quiz_getter,
                question=question,
                option1=option1,
                option2=option2,
                option3=option3,
                option4=option4,
                correct_answer=correct_answer
            )

        return redirect('dashboard')

    return render(request, 'quizform.html')       
            



def myquizzes_view(request):
    quizzes = Quiz.objects.filter(created_by=request.user)
    return render(request,'myquizes.html',{'quizzes':quizzes})


def delete_quiz(request,quiz_id):
    quiz_instance = get_object_or_404(Quiz, id=quiz_id, created_by=request.user)
    quiz_instance.delete()
    return redirect('myquiz')


def profile_view(request):
    user = request.user
    user_quizzes = Quiz.objects.filter(created_by=user)  
    context = {'username': user.username,'email': user.email,'quiz_count': user_quizzes.count()}

    return render(request, 'profile.html', context)



def takequiz_view(request, quiz_id):
    
    quiz_object = get_object_or_404(Quiz, id=quiz_id)
    list_of_questions = questions.objects.filter(quiz=quiz_object)
    total_questions = len(questions.objects.filter(quiz=quiz_object))
    quiz_object = get_object_or_404(Quiz, id = quiz_id)
    
    if request.method == "POST":
        score = 0
        
        for question in list_of_questions:
            is_correct=False
            selected_option = request.POST.get(f"question{question.id}")
            if selected_option and int(selected_option) == question.correct_answer:
                score += 1
                is_correct = True
            if is_correct:
                score_for_db=1
            else:
                score_for_db=0
            Answers.objects.create(
                    user=request.user,
                    quiz=quiz_object,
                    question=question,
                    selected_option=selected_option,
                    score=score_for_db
                    )

        attempts_object = Attempt.objects.create(user = request.user, quiz = quiz_object ,score = score)
        request.session['quiz_score'] = score
        return redirect('result', quiz_id=quiz_id)
    return render(request, 'take_quiz.html', {'quiz': quiz_object,'all_questions': list_of_questions,'total_questions': total_questions})



def result_view(request, quiz_id):
    quiz_object = get_object_or_404(Quiz, id=quiz_id)
    count_of_questions = len(questions.objects.filter(quiz = quiz_object))
    score = request.session.get('quiz_score', None)  
    return render(request, 'score.html', {'quiz': quiz_object, 'score': score, 'total_questions' : count_of_questions})



def allquiz_views(request):
    quizzes = Quiz.objects.all().order_by('created_at')
    return render(request,'allquiz.html',{'quizzes':quizzes})