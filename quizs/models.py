from django.db import models


# Create your models here.
# Quiz <-- Question <-- Answers models

class Quiz(models.Model):
    name = models.CharField(max_length=100, verbose_name="Quiz name")
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Question(models.Model):
    question_test = models.CharField(max_length=256, verbose_name="Question text")
    is_published = models.BooleanField(default=False)
    exam = models.ForeignKey(Quiz, related_name='questions', on_delete=models.SET_NULL)

    def __str__(self):
        return "{content} - {published}".format(content=self.question_test, published=self.is_published)


class Answer(models.Model):
    text = models.CharField(max_length=128, verbose_name='Answer\'s text')
    is_valid = models.BooleanField(default=False)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.SET_NULL)

    def __str__(self):
        return self.text
