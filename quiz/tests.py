from django.test import TestCase
from quiz.models import Quiz, Question, Answer


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


class AnswerTestCase(TestCase):
    def setUp(self):
        mocked_quiz = Quiz.objects.create(title="test_quiz")
        mocked_question = Question.objects.create(quiz=mocked_quiz,
                                                  question_text="test_question")
        Answer.objects.create(question=mocked_question,
                              answer_text="test_answer_text",
                              correct=True)

    def test_default_setting(self):
        mocked_question = Question.objects.get(question_text="test_question")
        answer = Answer.objects.get(question=mocked_question)
        self.assertEqual(answer.answer_text, "test_answer_text")
