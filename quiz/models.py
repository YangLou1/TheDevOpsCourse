from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    topic = models.CharField(max_length=50)
    points = models.IntegerField(default=10)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)
    correct = models.BooleanField()
