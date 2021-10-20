from typing import Tuple, List as List_
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from .forms import TaskForm, ListForm
from .models import List, Task


def _get_lists_and_current_list_number(request: HttpRequest, list_id: int) -> Tuple[List_[List], int]:
    """Returns user's lists list and current list user wants to modify if list_id is correct
    else returns user's lists and 0"""
    
    lists = List.objects.filter(user=request.user).order_by('-id')
    
    # try to get correct list. If failed - returns 0
    return (lists, list_id) if len(lists) > list_id else (lists, 0)


def _initialize_forms_if_needed(form_task: TaskForm, form_list: ListForm, for_list: List, user: User) -> Tuple[
    TaskForm, ListForm]:
    if form_task is None:
        form_task = TaskForm(for_list=for_list)
    if form_list is None:
        form_list = ListForm(user=user)
    
    return form_task, form_list


@login_required()
def new_task(request: HttpRequest, list_id: str) -> HttpResponse:
    """list_id = id of ordered by id lists of this user
    starts from 0
    
    After adding a task returns new task page with the same list, added task and
    previous tasks
    
    if list_id is incorrect - add task to the last created list."""
    
    # get all user lists and current list number that user want to modify
    lists, active_list = _get_lists_and_current_list_number(request, int(list_id))
    
    form_task = TaskForm(data=request.POST, for_list=lists[active_list])
    
    if form_task.is_valid():
        form_task.save()
        lists, _ = _get_lists_and_current_list_number(request, 0)
        return task_page_handler(request, lists, active_list)
    
    return task_page_handler(request, lists, active_list, form_task=form_task)


@login_required()
def task_page(request: HttpRequest):
    lists, active_list = _get_lists_and_current_list_number(request, 0)
    return view_for_no_lists(request) if (len(lists) == 0) else task_page_handler(request, lists, active_list)


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'home/home.html')


@login_required()
def new_list(request: HttpRequest) -> HttpResponse:
    form = ListForm(data=request.POST, user=request.user)
    lists, active_list = _get_lists_and_current_list_number(request, 0)
    
    if form.is_valid():
        form.save()
        return task_page_handler(request, lists, active_list)
    
    return task_page_handler(request, lists, active_list, form_list=form)


@login_required()
def activate_list(request: HttpRequest, list_id: str) -> HttpResponse:
    lists, active_list = _get_lists_and_current_list_number(request, int(list_id))
    return view_for_no_lists(request) if len(lists) == 0 else task_page_handler(request, lists, active_list)


@login_required()
def task_page_handler(request: HttpRequest,
                      lists: List_[List],
                      active_list: int,
                      form_task: TaskForm = None,
                      form_list: ListForm = None) -> HttpResponse:
    list_ = lists[active_list]
    tasks_list = Task.objects.all().filter(list=list_).order_by('-id')
    form_task, form_list = _initialize_forms_if_needed(form_task, form_list, list_, request.user)
    
    return render(request, 'lists/tasks.html', {'form_task': form_task,
                                                'form_list': form_list,
                                                'tasks_list': tasks_list,
                                                'active': active_list,
                                                'lists': lists,
                                                'header': list_.text})


@login_required()
def view_for_no_lists(request: HttpRequest) -> HttpResponse:
    form_list = ListForm(user=request.user)
    return render(request, 'lists/no_lists_page.html', {'form_list': form_list,
                                                        'header': 'No task lists found!\n Maybe you should create one?'})


@login_required()
def remove_list(request: HttpRequest, list_id: str) -> HttpResponse:
    # TODO: rewrite
    def delete_list(lists: List_[List], removed_list: id):
        try:
            lists[removed_list].delete()
            print('point two')
        except IndexError as e:
            print('ERROR!')
            pass
    
    
    lists, removed_list = _get_lists_and_current_list_number(request, int(list_id))
    delete_list(lists, removed_list)
    
    return view_for_no_lists(request) if len(lists) == 0 else task_page_handler(request, lists, 0)
