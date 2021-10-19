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
from .views import new_task, new_list, activate_list, task_page

# without lead-slash
urlpatterns = [
    path('', task_page, name='task_page'),
    path('add_list', new_list, name='add_list'),
    re_path(r'list(?P<list_id>\d+)', activate_list, name='activate_list'),
    re_path(r'add_task(?P<list_id>\d+)', new_task, name='new_task')
]
