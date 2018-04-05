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
    for i, question in enumerate(question_list):
        try:
            # get the selected answer's ID by checking its key name question.id
            selected_answer_id = request.POST[str(question.id)]
            # if the question is not answered
            if not selected_answer_id:
                raise KeyError
            # if the received answer is not valid
            if selected_answer_id not in [str(x.id) for x in Answer.objects.filter(question=question.id)]:
                raise Answer.DoesNotExist
            selected_answer = question.answer_set.get(pk=selected_answer_id)
        except KeyError:
            return render(request, 'quiz/question.html', {
                'question_list': question_list,
                'error_message': "You missed question #" + str(i+1)
            })
        except Answer.DoesNotExist:
            print("We got back a strange answer with invalid answer_id = " + selected_answer_id)
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
