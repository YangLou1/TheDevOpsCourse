from django.db import models


class Quiz(models.Model):
    num_questions = models.IntegerField(default=10)
    min_pass = models.IntegerField(default=10)
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz)
    question_text = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    topic = models.CharField(max_length=50)
    points = models.IntegerField(default=10)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)
    correct = models.BooleanField()

    def __str__(self):
        return self.answer_text
