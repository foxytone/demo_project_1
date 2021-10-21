from .models import List, Task, Data
from typing import Tuple, List as List_
from .forms import TaskForm, ListForm
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.db.models import QuerySet


def initialize_forms_if_needed(form_task: TaskForm, form_list: ListForm, for_list: List, user: User) -> Tuple[
    TaskForm, ListForm]:
    if form_task is None:
        form_task = TaskForm(for_list=for_list)
    if form_list is None:
        form_list = ListForm(user=user)
    
    return form_task, form_list


def set_active_user_list(request: HttpRequest, active_list: int, increment_lists: bool = False,
                         decrement_lists: bool = False):
    data, _ = Data.objects.update_or_create(user=request.user)
    
    if increment_lists:
        data.lists_count += 1
    
    if decrement_lists:
        data.lists_count -= 1
    
    if data.lists_count > active_list:
        data.last_active_list = active_list
    
    data.save()


def get_active_user_list_and_lists_count(request: HttpRequest) -> Tuple[int, int]:
    data, created = Data.objects.get_or_create(user=request.user)
    return data.last_active_list, data.lists_count


def remove_user(request: HttpRequest, removed_list: int):
    active_list, lists_count = get_active_user_list_and_lists_count(request)
    
    if lists_count > removed_list:
        
        if active_list > removed_list:
            active_list -= 1
        elif active_list == removed_list:
            active_list = 0
        
        set_active_user_list(request, active_list, decrement_lists=True)
        List.objects.filter(user=request.user).order_by('-id')[removed_list].delete()


def get_ordered_lists(request: HttpRequest) -> QuerySet[List]:
    return List.objects.filter(user=request.user).order_by('-id')


def get_ordered_tasks(list_: List) -> QuerySet[Task]:
    return Task.objects.filter(list=list_).order_by('-id')


def remove_task(list: List, ordered_task_id: int):
    tasks = get_ordered_tasks(list)
    if len(tasks) > ordered_task_id:
        tasks[ordered_task_id].delete()


def remove_task2(request: HttpRequest, active_list, task_id: int):
    list_ = get_ordered_lists(request)[active_list]
    task = Task.objects.filter(list=list_, id=task_id).first()
    if task is not None:
        task.delete()


def complite_task(request: HttpRequest, active_list, task_id: int):
    list_ = get_ordered_lists(request)[active_list]
    task = Task.objects.filter(list=list_, id=task_id).first()
    if task is not None:
        task.complited = not task.complited
        task.save()
