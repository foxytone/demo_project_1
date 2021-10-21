"""SimpleToDo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from .views import add_task, new_list, activate_list, task_page, remove_list, remove_task, mark_task

# without lead-slash
urlpatterns = [
    path('', task_page, name='task_page'),
    path('add_list', new_list, name='add_list'),
    path(r'add_task', add_task, name='add_task'),
    re_path(r'remove_list(?P<list_id>\d+)', remove_list, name='remove_list'),
    re_path(r'switch_list(?P<list_id>\d+)', activate_list, name='activate_list'),
    re_path(r'remove_task(?P<task_id>\d+)', remove_task, name='remove_task'),
    re_path(r'mark_task(?P<task_id>\d+)', mark_task, name='mark_task')

]
