from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView

from quizs.forms import TakeQuizForm, EditUserForm, EditExamineeForm, ExamineeSignUpForm
from quizs.models import TakenQuiz, Quiz, User


# Create your views here.


def home(request):
    if request.user.is_authenticated:
        if request.user.is_examinee:
            return redirect('examinee:quiz_list')
        else:
            return render(request, 'quizs/home.html')
    return render(request, 'quizs/home.html')


@login_required
def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'quizs/profile_detail.html', {'user': user})


@login_required
# @transaction.atomic
def edit_profile(request):
    if request.method == "POST":
        edit_user_form = EditUserForm(request.POST, instance=request.user)
        edit_profile_form = EditExamineeForm(request.POST, instance=request.user.examinee)
        if edit_user_form.is_valid() and edit_profile_form.is_valid():
            edit_user_form.save()
            edit_profile_form.save()
            return redirect(reverse('edit_profile'))
    else:
        edit_user_form = EditUserForm(instance=request.user)
        edit_profile_form = EditExamineeForm(instance=request.user.examinee)
        data = {
            'edit_user_form': edit_user_form,
            'edit_profile_form': edit_profile_form
        }
        return render(request, 'quizs/edit_profile.html', data)


class ExamineeSignUpView(CreateView):
    model = User
    form_class = ExamineeSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'examinee'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('examinee:quiz_list')


@method_decorator([login_required], name='dispatch')
class QuizListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'quizs/quiz_list.html'

    def get_queryset(self):
        examinee = self.request.user.examinee
        taken_quizzes = examinee.quizzes.values_list('pk', flat=True)
        queryset = Quiz.objects.filter() \
            .exclude(pk__in=taken_quizzes) \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset


@method_decorator([login_required], name='dispatch')
class TakenQuizListView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'quizs/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.examinee.taken_quizzes \
            .select_related('quiz') \
            .order_by('quiz__name')
        return queryset


@login_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    examinee = request.user.examinee

    if examinee.quizzes.filter(pk=pk).exists():
        return render(request, 'quizs/taken_quiz.html')

    total_questions = quiz.questions.count()
    unanswered_questions = examinee.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                examinee_answer = form.save(commit=False)
                examinee_answer.examinee = examinee
                examinee_answer.save()
                if examinee.get_unanswered_questions(quiz).exists():
                    return redirect('examinee:take_quiz', pk)
                else:
                    correct_answers = examinee.quiz_answers.filter(answer__question__quiz=quiz,
                                                                   answer__is_correct=True).count()
                    score = round((correct_answers / total_questions) * 100.0, 2)
                    TakenQuiz.objects.create(examinee=examinee, quiz=quiz, score=score)
                    if score < 50.0:
                        messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (
                            quiz.name, score))
                    else:
                        messages.success(request,
                                         'Congratulations! You completed the quiz %s with success! You scored %s '
                                         'points.' % (
                                             quiz.name, score))
                    return redirect('examinee:quiz_list')
    else:
        form = TakeQuizForm(question=question)

    return render(request, 'quizs/take_quiz_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': progress
    })
