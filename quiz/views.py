from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Question, Answer, Quiz


def index(request):
    quiz_list = Quiz.objects.all()
    context = {'quiz_list': quiz_list}
    return render(request, 'quiz/index.html', context)


def detail(request, quiz):
    question_list = Question.objects.filter(quiz=quiz)
    context = {'question_list': question_list}
    return render(request, 'quiz/question.html', context)


def submit(request, quiz):
    request.session['score'] = 0
    request.session['total_points'] = 0
    question_list = Question.objects.filter(quiz=quiz)
    for question in question_list:
        try:
            selected_answer_id = request.POST[str(question.id)]
            selected_answer = question.answer_set.get(pk=selected_answer_id)
        except (KeyError, Answer.DoesNotExist):
            return render(request, 'quiz/question.html', {
                'question_list': question_list,
                'error_message': "Please answer all the questions before submitting.",
            })
        else:
            request.session['total_points'] += question.points
            if selected_answer.correct:
                request.session['score'] += question.points
    return HttpResponseRedirect('result')


def result(request, quiz):
    record = {'quiz_id': quiz,
              'score': request.session['score'],
              'total_points': request.session['total_points'],
              'pass': True if request.session['score'] >= Quiz.objects.get(id=quiz).min_pass else False}
    return render(request, 'quiz/result.html', record)


