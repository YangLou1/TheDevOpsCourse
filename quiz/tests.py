from django.test import TestCase
from quiz.models import Quiz


class QuizTestCase(TestCase):
    def setUp(self):
        Quiz.objects.create(title="test")

    def test_default_setting(self):
        q = Quiz.objects.get(title="test")
        self.assertEqual(q.num_questions, 10)
        self.assertEqual(q.min_pass, 10)
