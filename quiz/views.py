from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Question, Answer, Quiz

try:
    from typing import List, Any, Dict, Union
except ImportError:
    print("WARNING: Typing module is not find")


def index(request: HttpRequest) -> object:
    quiz_list = Quiz.objects.all()  # type: List[Quiz]
    context = {'quiz_list': quiz_list}  # Dict[str,List[Quiz]]
    return render(request, 'quiz/index.html', context)


def detail(request: HttpRequest, quiz: Quiz) -> object:
    progress = request.session.get('progress', 1)  # type: int
    if int(quiz) > progress:
        return render(request, 'quiz/question.html', {
            'error_message': "You cannot take this quiz!"
        })
    question_list = Question.objects.filter(quiz=quiz)  # type: List[Question]
    context = {'question_list': question_list}  # type: Dict[str,List[Question]]
    return render(request, 'quiz/question.html', context)


def submit(request: HttpRequest, quiz: Quiz) -> object:
    request.session['score'] = 0
    request.session['total_points'] = 0
    question_list = Question.objects.filter(quiz=quiz)  # type: List[Question]
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
                'error_message': "You missed question #" + str(i + 1)
            })
        except Answer.DoesNotExist:
            print("We got back a strange answer with invalid answer_id = " + selected_answer_id)
        else:
            request.session['total_points'] += question.points
            if selected_answer.correct == '1':
                request.session['score'] += question.points
    return HttpResponseRedirect('result')


def result(request: HttpRequest, quiz: Quiz) -> object:
    passed = True if request.session['score'] >= Quiz.objects.get(id=quiz).min_pass else False
    # If the quiz got passed and it is not a repeated submission, accumulate the progress number.    
    if passed and request.session['progress'] == int(quiz):
        request.session['progress'] += 1
    record = {'quiz_id': quiz,
              'score': request.session['score'],
              'total_points': request.session['total_points'],
              'pass': passed,
              'progress': request.session['progress']}  # type: Dict[str,Union[Quiz,int,bool,object]]
    return render(request, 'quiz/result.html', record)


def lesson(request: HttpRequest, lesson: str) -> object:
    """
    Right now, hard code the two quizzes' relationship. The progress number,
    which is the same as the quiz_id, mark the user's current progress
    in that lesson.
    """

    template_path = 'quiz/lesson' + lesson + '.html'  # type: str
    progress = request.session.get('progress', 1)  # type: int
    if progress >= 3:
        progress = 1
    request.session['progress'] = progress
    try:
        if not Quiz.objects.get(pk=progress):
            raise Quiz.DoesNotExist
        # if user have submitted the lesson's quiz and then retake the same lesson
        if int(lesson[0]) < progress:
            quiz_id = int(lesson[0])
        # if the lesson's number is equal to the progress number
        else:
            quiz_id = progress
        context = {'quiz': Quiz.objects.get(pk=quiz_id)}  # type: Dict[str,List[Quiz]]
    except Quiz.DoesNotExist:
        return render(request, template_path, {
            'error_message': "Unable to get quiz #" + request.session['progress']
        })
    return render(request, template_path, context)
