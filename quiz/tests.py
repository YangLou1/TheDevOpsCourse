from django.test import TestCase
from quiz.models import Quiz, Question


class QuizTestCase(TestCase):
    def setUp(self):
        Quiz.objects.create(title="test")

    def test_default_setting(self):
        q = Quiz.objects.get(title="test")
        self.assertEqual(q.num_questions, 10)
        self.assertEqual(q.min_pass, 10)


class QuestionTestCase(TestCase):
    def setUp(self):
        mocked_quiz = Quiz.objects.create(title="test")
        Question.objects.create(quiz=mocked_quiz, question_text="test")

    def test_default_setting(self):
        mocked_quiz = Quiz.objects.get(title="test")
        question = Question.objects.get(quiz=mocked_quiz)
        self.assertEqual(question.question_text, "test")
