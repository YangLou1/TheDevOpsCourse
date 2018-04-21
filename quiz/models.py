from django.db import models


class Quiz(models.Model):
    num_questions = models.IntegerField(default=10)  # type: int
    min_pass = models.IntegerField(default=10)  # type: int
    title = models.CharField(max_length=50)  # type: str

    def __str__(self)->str:
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz)
    question_text = models.CharField(max_length=200)  # type: str
    type = models.CharField(max_length=50)  # type: str
    topic = models.CharField(max_length=50)  # type: str
    points = models.IntegerField(default=10)  # type: int

    def __str__(self)->str:
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)  # type: str
    correct = models.BooleanField()  # type: bool

    def __str__(self)->str:
        return self.answer_text
