# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
import json

from task.models import Task
from task.forms import LoginForm, SignupForm, TaskForm


def anonymous_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(kwargs.get('next', reverse('task')))
        return func(request, *args, **kwargs)
    return wrapper

def login_required_ajax(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return func(request, *args, **kwargs)
        elif request.is_ajax():
            return HttpResponseAjaxError(
                code = "no_auth",
                message = u'Требуется авторизация',
            )
        else:
            return redirect('/login/')
    return wrapper


@anonymous_required
def index(request):
    return render(request, 'index.html')

@anonymous_required
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('task'))
    else:
        form = LoginForm()

    return render(request, 'login.html', {
        'form': form,
    })

@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

@anonymous_required
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {
        'form': form,
    })

@login_required(login_url='/login/')
def task(request):
    tasks = Task.objects.exclude(is_done=True).order_by('estimate')

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form._user = request.user
            task = form.save()
            return HttpResponseRedirect(reverse('task'))
    else:
        form = TaskForm()

    return render(request, 'task.html', {
        'tasks': tasks,
        'form': form,
        'user': request.user,
    })

@login_required_ajax
def add_task(request):
    if request.method == 'POST' and request.is_ajax():
        form = TaskForm(request.POST)
        if form.is_valid():
            form._user = request.user
            task = form.save()
            return render(request,'task_item.html', {
                'task': task
            })
    else:
        return JsonResponse({
            'status': 'Fail',
            'msg': 'Not valid request'
        })

@login_required_ajax
def task_complete(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            task = Task.objects.filter(
                        pk=request.POST['id'],
                        user=request.user) \
                    .update(is_done=True)
            return JsonResponse({
                'code': 200,
                'msg': 'save successfully'
            })
        except Task.DoesNotExist:
            return JsonResponse({
                'code': 404,
                'msg': 'Object does not exist'
            })
    else:
        return JsonResponse({
            'code': 400,
            'msg':'Not a valid request'
        })

@login_required_ajax
def task_detail(request):
    if request.method == 'GET' and request.is_ajax():
        task = get_object_or_404(Task,
                    pk=request.GET['id'],
                    user=request.user)
        return render(request,'task_detail.html', {
            'task': task
        })
    else:
        return JsonResponse({
            'status': 'Fail',
            'msg': 'Not valid request'
        })