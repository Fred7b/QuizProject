# Register your models here.
import nested_admin
from django.contrib import admin

from .models import Quiz, Question, Answer


class AnswerInline(nested_admin.NestedStackedInline):
    model = Answer
    extra = 1


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    extra = 1
    inlines = [AnswerInline]


class QuizAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline]


admin.site.register(Quiz, QuizAdmin)