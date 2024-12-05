from django.shortcuts import render

import json
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.db import IntegrityError
from .models import User, Task, SubTask

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.core.paginator import Paginator


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    page = request.GET.get("page", 1)
    print(page)
    return render(request, "tasker/index.html", {
        "page":page,
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if not user:
            return render(request, "tasker/login.html", {
                "message": "Entered Invalid Credentials",
            })
        
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "tasker/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("login")


def register_view(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, "tasker/register.html", {
                "message":"Password and Confirm Password didn't match",
            })
        
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "tasker/register.html", {
                "message":"Username already taken."
            })
        
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "tasker/register.html")


# View for showing new task form and adding a new task
@csrf_exempt
@login_required(login_url="/login")
def new_task(request):
    if request.method == "POST":
        try:
            task = json.loads(request.body)
            task_obj = Task.objects.create(
                user = request.user,
                task_name = task["name"],
                description = task["description"],
                is_important = task["important"],
                is_urgent = task["urgent"],
            )

            for subtask in task['subtasks']:
                SubTask.objects.create(
                    parent_task = task_obj,
                    subtask_name = subtask
                )

            return JsonResponse({"result":"success", "message": "Task Recieved successfully.", "task": task_obj.serialize() }, status=201)
        
        except Exception as e:
            print(e)
            return JsonResponse({"error":"No data/ Invalid data recieved"}, status=404)

    return render(request, "tasker/new_task.html", {})


# Delete task view
@login_required(login_url="/login")
def delete_task(request, id):
    Task.objects.get(pk=id).delete()
    return HttpResponseRedirect(reverse("index"))


# Show task view
@login_required(login_url="/login")
def show_task(request, id):
    task = Task.objects.get(pk = id)
    return render(request, "tasker/show_task.html", {
        "task":task,
    })


# Priority Matrix view
@login_required(login_url="/login")
def priority_matrix(request):
    priority1_tasks_cnt = request.user.tasks.filter(is_important=True).filter(is_urgent=True).count()
    priority2_tasks_cnt = request.user.tasks.filter(is_important=True).filter(is_urgent=False).count()
    priority3_tasks_cnt = request.user.tasks.filter(is_important=False).filter(is_urgent=True).count()
    priority4_tasks_cnt = request.user.tasks.filter(is_important=False).filter(is_urgent=False).count()
    return render(request, "tasker/priority_matrix.html", {
        "priority1_cnt": priority1_tasks_cnt,
        "priority2_cnt": priority2_tasks_cnt,
        "priority3_cnt": priority3_tasks_cnt,
        "priority4_cnt": priority4_tasks_cnt,
    })


# Priority tasks showing view
@login_required(login_url="/login")
def show_priority_tasks(request, priority):
    title = ""
    if priority == 1:
        title = "Important and Urgent"
    elif priority == 2:
        title = "Important and Not Urgent"
    elif priority == 3:
        title = "Not Important and Urgent"
    elif priority == 4:
        title = "Not Important and Not Urgent"
    elif priority > 4:
        return HttpResponse(status=404)
    
    page = request.GET.get("page") or 1

    return render(request, "tasker/show_priority_tasks.html", { 
        "page_title": title, 
        "priority":priority,
        "page": page
    })


# User Profile page view
@login_required
def user_profile(request):
    completed = [task for task in request.user.tasks.all() if task.get_progress == 100]
    priority1_tasks = request.user.tasks.filter(is_important=True).filter(is_urgent=True).all()
    priority2_tasks = request.user.tasks.filter(is_important=True).filter(is_urgent=False).all()
    priority3_tasks = request.user.tasks.filter(is_important=False).filter(is_urgent=True).all()
    priority4_tasks = request.user.tasks.filter(is_important=False).filter(is_urgent=False).all()

    priority1_tasks_completed = [task for task in priority1_tasks if task.get_progress == 100]
    priority2_tasks_completed = [task for task in priority2_tasks if task.get_progress == 100]
    priority3_tasks_completed = [task for task in priority3_tasks if task.get_progress == 100]
    priority4_tasks_completed = [task for task in priority4_tasks if task.get_progress == 100]
    return render(request, "tasker/profile.html", {
        "completed_count": len(completed),
        "priority1_tasks_count": priority1_tasks.count(),
        "priority2_tasks_count": priority2_tasks.count(),
        "priority3_tasks_count": priority3_tasks.count(),
        "priority4_tasks_count": priority4_tasks.count(),

        "priority1_completed_tasks_count": len(priority1_tasks_completed),
        "priority2_completed_tasks_count": len(priority2_tasks_completed),
        "priority3_completed_tasks_count": len(priority3_tasks_completed),
        "priority4_completed_tasks_count": len(priority4_tasks_completed),
    })




# API VIEWS
# Get preview contents of all tasks
@login_required(login_url="/login")
def api_tasks(request):
    tasks = request.user.tasks.order_by("-updated").all()

    page = request.GET.get("page") or 1
    tasks = Paginator(tasks, per_page=6)

    serialized = [task.preview_serialize() for task in tasks.get_page(page)]
    return JsonResponse({
        "tasks":serialized,
        "page": page,
        "has_next": tasks.get_page(page).has_next(),
        "has_previous": tasks.get_page(page).has_previous()
    })


# Get/Update the contents of a task
@csrf_exempt
@login_required(login_url="/login")
def api_task(request, id):
    try:
        task = Task.objects.get(pk = id)
    except Task.DoesNotExist:
        return JsonResponse({"error":"Task Not Found"}, status = 404)
    
    # Return Task Contents
    if request.method == "GET":
        return JsonResponse(task.serialize(), status = 201)
    
    # Update the task if put request
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("description"):
            task.description = data["description"]
        if data.get("urgent") is not None:
            task.is_urgent = data["urgent"]
        if data.get("important") is not None:
            task.is_important = data["important"]
        
        task.save()
        return JsonResponse({
            "result": "Task updated successfully",
            "task": task.task_name
        }, status=201)
    
    return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


# API view for getting tasks having a given priority
@login_required(login_url="/login")
def api_priority_tasks(request, priority):
    tasks = request.user.tasks
    if priority == 1:
        tasks = tasks.filter(is_important=True).filter(is_urgent=True).order_by("-updated").all()
    elif priority == 2:
        tasks = tasks.filter(is_important=True).filter(is_urgent=False).order_by("-updated").all()
    elif priority == 3:
        tasks = tasks.filter(is_important=False).filter(is_urgent=True).order_by("-updated").all()
    elif priority == 4:
        tasks = tasks.filter(is_important=False).filter(is_urgent=False).order_by("-updated").all()
    else:
        return JsonResponse({"error":"Invalid Priority"}, status=404)
    
    page = request.GET.get("page") or 1
    tasks = Paginator(tasks, per_page=6)

    serialized = [task.preview_serialize() for task in tasks.get_page(page)]
    return JsonResponse({
        "tasks":serialized,
        "page": page,
        "has_next": tasks.get_page(page).has_next(),
        "has_previous": tasks.get_page(page).has_previous()
    })


# API view for adding a new subtask
@csrf_exempt
@login_required(login_url="/login")
def api_add_subtask(request):
    if request.method == "POST":
        data = json.loads(request.body)
        parent_id = data["taskid"]
        subtask_name = data["subtask_name"]

        parent_task = Task.objects.get(pk=parent_id)
    
        subtask = SubTask.objects.create(
            subtask_name = subtask_name,
            parent_task = parent_task,
        )

        parent_task.save()

        return JsonResponse({
            "result":"Sucessfully added Subtask",
            "new_progress":subtask.parent_task.get_progress,
            "subtask": subtask.serialize(),
        }, status=201)
    
    return JsonResponse({"error":"POST Request Required"}, status=400)


# Delete/Update the subtask
@csrf_exempt
@login_required(login_url="/login")
def api_subtask(request, id):
    subtask = SubTask.objects.get(pk = id)

    if request.method == "DELETE":
        subtask.parent_task.save() # saving the parent so it get's updated
        subtask.delete()
        return JsonResponse({
            "result":"Sucessfully deleted Subtask",
            "new_progress":subtask.parent_task.get_progress,
        }, status=201)
    
    if request.method == "PUT":
        data = json.loads(request.body)
        subtask.completed = data["completed"]
        
        subtask.save()
        subtask.parent_task.save()
        return JsonResponse({
            "result":f"{subtask.subtask_name} is completed: {subtask.completed}", 
            "new_progress": subtask.parent_task.get_progress
        }, status = 201)

    return JsonResponse({"error":"PUT or DELETE request is required"}, status=400)
