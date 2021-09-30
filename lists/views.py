from django.shortcuts import render
from .forms import TaskForm
from .models import List, Task


# Create your views here.

def tasks_view(request, list_: List = None):
    form = TaskForm(list_=List(text='none!'))
    return render(request, 'tasks.html', {'form': form})


def new_task(request):
    form = TaskForm(data=request.POST, for_list=List.objects.create('A new list!'))
    if form.is_valid():
        counter = List.objects.count()
        list_ = List.objects.create(text=f'{counter + 1}')

    return render(request, 'base.html')
