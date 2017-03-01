# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import Question, Answer


class AskForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self._user = None
        super(AskForm, self).__init__(*args, **kwargs)

    title = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.Textarea)

    def clean_title(self):
        title = self.cleaned_data['title']
        if title == '':
            raise forms.ValidationError('Поле с заголовком не может быть пустым')
        return title

    def clean_text(self):
        text = self.cleaned_data['text']
        if text == '':
            raise forms.ValidationError('Поле с текстом не может быть пустым')
        return text

    def clean(self):
        return self.cleaned_data

    def save(self):
        self.cleaned_data['author'] = self._user
        return Question.objects.create(**self.cleaned_data)


class AnswerForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self._user = None
        super(AnswerForm, self).__init__(*args, **kwargs)

    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField()

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text) == 0:
            raise forms.ValidationError('Поле с текстом не может быть пустым', code="text_error")
        return text

    def clean_question(self):
        question = int(self.cleaned_data['question'])
        if Question.objects.filter(pk=question).count() == 0:
            raise forms.ValidationError('Отправлен урл не по тому запросу', code="question_error")
        if question <= 0:
            raise forms.ValidationError("Номер вопрос не может быть <= 0")
        return question

    def clean(self):
        return self.cleaned_data

    def save(self):
        return Answer.objects.create(text=self.cleaned_data['text'],
                                     question_id=self.cleaned_data['question'],
                                     author=self._user)


class SignupForm(forms.Form):
    username = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 3:
            raise forms.ValidationError('Username is too small')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 3:
            raise forms.ValidationError('Password is too small')
        return password

    def save(self):
        return User.objects.create_user(**self.cleaned_data)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 3:
            raise forms.ValidationError('Username is too small')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 3:
            raise forms.ValidationError('Password is too small')
        return password

    def clean(self):
        user = authenticate(username=self.cleaned_data['username'],
                            password=self.cleaned_data['password'])
        if not user:
            raise forms.ValidationError('The username or password is wrong!')

        if user and not user.is_active:
            raise forms.ValidationError('This user is not active')

        return self.cleaned_data

    def save(self):
        return authenticate(username=self.cleaned_data['username'],
                            password=self.cleaned_data['password'])