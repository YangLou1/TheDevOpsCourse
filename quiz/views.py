from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from .models import Question, Answer


score = 0
total_points = 0


def index(request):
    question_list = Question.objects.all()
    context = {'question_list': question_list}
    return render(request, 'quiz/index.html', context)


def submit(request):
    global score, total_points 
    score = 0
    total_points = 0

    question_list = Question.objects.all()

    for question in question_list:
        try:
            selected_answer_id = request.POST[str(question.id)]
            selected_answer = question.answer_set.get(pk=selected_answer_id)
        except (KeyError, Answer.DoesNotExist):
            return render(request, 'quiz/index.html', {
                'question_list': question_list,
                'error_message': "Please answer all the questions before submitting.",
            })
        else:             
            total_points += question.points
            if selected_answer.correct:
                score += question.points

    return HttpResponseRedirect('result')


def result(request):   
    global score, total_points      
    result = {'score': score, 'total_points': total_points}   
    score = 0
    total_points = 0
    return render(request, 'quiz/result.html', result)


