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
    passed = True if request.session['score'] >= Quiz.objects.get(id=quiz).min_pass else False
    # If the quiz got passed and it is not a repeated submission, accumulate the progress number.
    if passed and request.session['progress'] == int(quiz):
        request.session['progress'] += 1
    record = {'quiz_id': quiz,
              'score': request.session['score'],
              'total_points': request.session['total_points'],
              'pass': passed,
              'progress': request.session['progress']}
    print(quiz, request.session['progress'])
    return render(request, 'quiz/result.html', record)


def lesson(request):
    """
    Right now, hard code the two quizzes' relationship. The progress number,
    which is the same as the quiz_id, mark the user's current progress
    in that lesson.
    """
    progress = request.session.get('progress', 1)
    if progress >= 3:
        progress = 1
    request.session['progress'] = progress
    print(progress)
    try:
        if not Quiz.objects.get(pk=progress):
            raise Quiz.DoesNotExist
        context = {'quiz': Quiz.objects.get(pk=progress)}
    except Quiz.DoesNotExist:
        return render(request, 'quiz/material.html', {
            'error_message': "Unable to get quiz #" + request.session['progress']
        })
    return render(request, 'quiz/material.html', context)
