from django.shortcuts import render, redirect
from .forms import TaskForm, ListForm
from .models import List, Task
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from typing import Tuple, List as List_


@login_required()
def new_task(request: HttpRequest, list_id):
    active_list = int(list_id)
    list_ = List.objects.all().filter(user=request.user).order_by('-time_created')[active_list]

    form_task = TaskForm(data=request.POST, for_list=list_)
    if form_task.is_valid():
        form_task.save()
        return redirect('task_page')
    # TODO order by id obv
    lists = List.objects.all().filter(user=request.user).order_by('-time_created')
    form_list = ListForm(user=request.user)
    tasks_list = Task.objects.all().filter(list=list_)

    return render(request, 'lists/tasks.html', {'form_task': form_task,
                                                'form_list': form_list,
                                                'tasks_list': tasks_list,
                                                'active': active_list,
                                                'lists': lists,
                                                'header': list_.text})


def home(request: HttpRequest):
    return render(request, 'home/home.html')


@login_required()
def new_list(request: HttpRequest):
    form = ListForm(data=request.POST, user=request.user)
    if form.is_valid():
        form.save()
        return redirect('task_page')

    return redirect('task_page')


@login_required()
def activate_list(request: HttpRequest, list_id: int):
    id_list = int(list_id)

    return task_page(request, active_list=id_list)


@login_required()
def _create_new_list(request: HttpRequest) -> Tuple[List_[List], int]:
    list_ = [List.objects.create(text='My new list!',
                                 user=request.user)]
    active = 0
    return list_, active


@login_required()
def task_page(request: HttpRequest, active_list: int = 0):
    list_ = List.objects.all().filter(user=request.user).order_by('-time_created')
    if len(list_) == 0:
        return view_for_no_lists(request)

    tasks_list = Task.objects.all().filter(list=list_[active_list]).order_by('-time_created')
    form_task = TaskForm(for_list=list_[active_list], active_list=active_list)
    form_list = ListForm(user=request.user)
    return render(request, 'lists/tasks.html', {'form_task': form_task,
                                                'form_list': form_list,
                                                'tasks_list': tasks_list,
                                                'active': active_list,
                                                'lists': list_,
                                                'header': list_[active_list].text})


def view_for_no_lists(request: HttpRequest):
    form_list = ListForm(user=request.user)
    return render(request, 'lists/no_lists_page.html', {'form_list': form_list,
                                                        'header': 'No task lists found!\n Maybe you should create one?'})
