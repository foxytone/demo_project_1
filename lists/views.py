from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .forms import TaskForm, ListForm
from .support import remove_user, set_active_user_list, get_active_user_list_and_lists_count, \
    initialize_forms_if_needed, get_ordered_lists, get_ordered_tasks, remove_task, remove_task2, complite_task


@login_required()
def add_task(request: HttpRequest) -> HttpResponse:
    active_list, _ = get_active_user_list_and_lists_count(request)
    list_ = get_ordered_lists(request)[active_list]
    form_task = TaskForm(data=request.POST, for_list=list_)
    
    if form_task.is_valid():
        form_task.save()
        return redirect('task_page')
    
    return task_page(request, form_task=form_task)


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'home/home.html')


@login_required()
def new_list(request: HttpRequest) -> HttpResponse:
    form = ListForm(data=request.POST, user=request.user)
    
    if form.is_valid():
        form.save()
        set_active_user_list(request, 0, increment_lists=True)
        return redirect('task_page')
    
    return task_page(request, form_list=form)


@login_required()
def activate_list(request: HttpRequest, list_id: str) -> HttpResponse:
    set_active_user_list(request, int(list_id))
    return redirect('task_page')


@login_required()
def task_page(request: HttpRequest,
              form_task: TaskForm = None,
              form_list: ListForm = None) -> HttpResponse:
    active_list, lists_count = get_active_user_list_and_lists_count(request)
    
    if lists_count == 0:
        return view_for_no_lists(request)
    
    lists = get_ordered_lists(request)
    list_ = lists[active_list]
    tasks = get_ordered_tasks(list_)
    form_task, form_list = initialize_forms_if_needed(form_task, form_list, list_, request.user)
    
    return render(request, 'lists/tasks.html', {'form_task': form_task,
                                                'form_list': form_list,
                                                'tasks': tasks,
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
    remove_user(request, int(list_id))
    return redirect('task_page')


@login_required()
def remove_task(request: HttpRequest, task_id: str) -> HttpResponse:
    active_list, lists_count = get_active_user_list_and_lists_count(request)
    if lists_count == 0:
        return view_for_no_lists(request)
    
    remove_task2(request, active_list, int(task_id))
    return redirect('task_page')


@login_required()
def mark_task(request: HttpRequest, task_id: str) -> HttpResponse:
    active_list, lists_count = get_active_user_list_and_lists_count(request)
    if lists_count == 0:
        return view_for_no_lists(request)
    
    complite_task(request, active_list, int(task_id))
    return redirect('task_page')
