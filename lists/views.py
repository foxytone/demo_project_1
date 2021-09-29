from django.shortcuts import render
from .forms import TaskForm


# Create your views here.

def tasks_view(request):
    form = TaskForm
    return render(request, 'tasks.html', {'form': form})
