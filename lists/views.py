from django.shortcuts import render


# Create your views here.

def tasks_view(request):
    return render(request, 'tasks.html')
