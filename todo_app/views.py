from django.shortcuts import render, redirect, get_object_or_404
from .models import Task

def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'todo_app/task_list.html', {'tasks': tasks})

def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Task.objects.create(title=title)
        return redirect('task_list')
    return render(request, 'todo_app/task_form.html')

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        if 'completed' in request.POST:
            task.completed = not task.completed
            task.save()
        elif 'title' in request.POST:
             task.title = request.POST.get('title')
             task.save()
        return redirect('task_list')
    return render(request, 'todo_app/task_form.html', {'task': task})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return redirect('task_list')
