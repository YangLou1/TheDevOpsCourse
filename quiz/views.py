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
    lower_answer_id = 1
    question_list = Question.objects.filter(quiz=quiz)
    for question in question_list:
        upper_answer_id = lower_answer_id + Answer.objects.filter(question=question.id).count() - 1
        try:
            # get the selected answer's ID by checking its key name question.id
            selected_answer_id = request.POST[str(question.id)]
            # selected_answer_id is an empty string if the question is not answered
            if selected_answer_id == '':
                raise KeyError
            # if selected_answer_id is not valid and not submitted by the user filling in the form
            elif int(selected_answer_id) < lower_answer_id or int(selected_answer_id) > upper_answer_id:   
                raise Answer.DoesNotExist
            else:
                selected_answer = question.answer_set.get(pk=selected_answer_id)
        except KeyError:
            return render(request, 'quiz/question.html', {
                'question_list': question_list,
                'error_message': "Hey, you forgot to answer question #" + str(question.id),
            })
        except Answer.DoesNotExist:
            print("We got back a strange answer with invalid answer_id = " + selected_answer_id)   
        else:
            request.session['total_points'] += question.points
            if selected_answer.correct:
                request.session['score'] += question.points
            lower_answer_id = upper_answer_id + 1
    return HttpResponseRedirect('result')


def result(request, quiz):
    record = {'quiz_id': quiz,
              'score': request.session['score'],
              'total_points': request.session['total_points'],
              'pass': True if request.session['score'] >= Quiz.objects.get(id=quiz).min_pass else False}
    return render(request, 'quiz/result.html', record)


