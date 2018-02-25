from django.shortcuts import get_object_or_404, render, HttpResponse
from .models import Question, Answer


def index(request):
    question_list = Question.objects.all()
    context = {'question_list': question_list}
    return render(request, 'quiz/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'quiz/detail.html', {'question': question})


def submit(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_answer = question.answer_set.get(pk=request.POST['answer'])
    except (KeyError, Answer.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'quiz/detail.html', {
            'question': question,
            'error_message': "You didn't select an answer.",
        })
    else:
        if selected_answer.correct:
            return HttpResponse('YES')
        else:
            return HttpResponse('NO')
