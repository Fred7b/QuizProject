from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from .models import (Answer, Question, Examinee, ExamineeAnswer,
                     User)


class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user


class ExamineeSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_examinee = True
        user.save()
        examinee = Examinee.objects.create(user=user)

        return user


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text',)


class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')


class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = ExamineeAnswer
        fields = ('answer',)

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

    username = forms.CharField(label="Ник",
                               widget=forms.TextInput(attrs={'placeholder': 'Ник',
                                                             'class': 'form-control', }))
    email = forms.EmailField(label="E-Mail",
                             widget=forms.EmailInput(attrs={'placeholder': 'E-Mail',
                                                            'class': 'form-control'}))


class EditExamineeForm(forms.ModelForm):
    class Meta:
        model = Examinee
        fields = ('gender', 'about_me',)

    gender = forms.ChoiceField(label="Выберите пол", choices=Examinee.GENDER_CHOICES,
                               widget=forms.Select(attrs={'class': 'form-control'}))
