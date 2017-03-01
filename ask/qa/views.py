from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

# Create your views here.
from django.views.decorators.http import require_GET

from .forms import AskForm, AnswerForm, SignupForm, LoginForm
from .utils.shortcut_pagination import paginate
from .models import Question, Answer


def test(request, *args, **kwargs):
    return HttpResponse('OK')


@require_GET
@login_required(login_url='/login/')
def index(request):
    questions = Question.objects.new()
    page, paginator = paginate(request, questions)
    paginator.baseurl = '/?page='
    return render(request, 'index.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page
    })


@require_GET
def popular_questions(request):
    questions = Question.objects.popular()
    page, paginator = paginate(request, questions)
    paginator.baseurl = '/popular/?page='
    return render(request, 'index.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page
    })


@login_required(login_url='/login/')
def show_question(request, id):
    question = get_object_or_404(Question, id=id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        form._user = request.user
        if form.is_valid():
            answer = form.save()
            url = answer.question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm()
        form._user = request.user
    answers = Answer.objects.filter(question=question)
    return render(request, 'question.html', {
        'question': question,
        'answers': answers,
        'form': form,
        'user': request.user
    })


@login_required(login_url='/login/')
def add_ask(request):
    print(request.session.get('sessionid'))
    if request.method == 'POST':
        form = AskForm(request.POST)
        form._user = request.user
        if form.is_valid():
            question = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
        form._user = request.user
    return render(request, 'add_ask.html', {
        'form': form
    })


def signup_controller(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(form.cleaned_data['password'])
            authenticated_user = \
                authenticate(username=user.username, password=form.cleaned_data['password'])
            login(request, authenticated_user)
            return HttpResponseRedirect('/')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {
        'form': form
    })


def login_controller(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/')

    form = LoginForm()
    return render(request, 'login.html', {
        'form': form
    })


def logout_controller(request):
    logout(request)
    return redirect('login')
