from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_examinee = models.BooleanField(default=False)


class Quiz(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField('Question', max_length=255)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return self.text


class Examinee(models.Model):
    GENDER_CHOICES = (
        ("UNSPECIFIED", "unspecified"),
        ("MALE", "Male"),
        ("FEMALE", "Female"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
    gender = models.CharField(verbose_name='Пол', max_length=20, choices=GENDER_CHOICES, default="UNSPECIFIED", )
    about_me = models.TextField(verbose_name="о себе", max_length=500)
    # asd = models.TextField()

    def get_unanswered_questions(self, quiz):
        answered_questions = self.quiz_answers \
            .filter(answer__question__quiz=quiz) \
            .values_list('answer__question__pk', flat=True)
        questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text')
        return questions

    def __str__(self):
        return self.user.username


class TakenQuiz(models.Model):
    examinee = models.ForeignKey(Examinee, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)


class ExamineeAnswer(models.Model):
    examinee = models.ForeignKey(Examinee, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')
