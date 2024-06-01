from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from .models import User, Post
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json

def index(request):
    all_posts = Post.objects.all().order_by("-date_created")
    posts =  Paginator(all_posts, per_page=10)
    page = request.GET.get("page") or 1
    return render(request, "network/index.html", {
        "posts":posts.get_page(page),
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def user_profile(request, username):
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("User with this Username Doesn't Exist")
    
    all_posts = profile_user.posts.order_by("-date_created")
    posts = Paginator(all_posts, per_page=10)
    page = request.GET.get("page") or 1
    
    follows = (request.user.is_authenticated and request.user.following.filter(username=username) )

    return render(request, "network/user_profile.html", {
        "profile_user":profile_user,
        "posts": posts.get_page(page),
        "follows": follows,
    })


def following(request):
    all_posts = Post.objects     \
            .filter(poster__in = request.user.following.all())      \
            .order_by("-date_created")
    posts = Paginator(all_posts, per_page=10)
    page = request.GET.get("page") or 1
    return render(request, "network/following_page.html", { 
        "posts": posts.get_page(page)
    })



@login_required(login_url="/login")
def create_post(request):
    if request.method == "POST":
        content = request.POST["content"]
        if content == "":
            return render(request, "network/create_post.html", {
                "message": " Please add some content before submitting Post",
            })
        Post.objects.create(
            poster = request.user,
            content = content,
        )

    return render(request, "network/create_post.html")


@login_required(login_url='/login')
def follow(request, username):
    profile_user = User.objects.get(username=username)
    profile_user.followers.add(request.user)
    return HttpResponseRedirect(reverse("user_profile", args=(username,) ))

@login_required(login_url='/login')
def unfollow(request, username):
    profile_user = User.objects.get(username=username)
    profile_user.followers.remove(request.user)
    return HttpResponseRedirect(reverse("user_profile", args=(username,) ))


# View to Update a edited Post
@csrf_exempt
@login_required(login_url='/login')
def update_post(request, post_id):
    if request.method != "PUT":
        return JsonResponse({"result":"Failed" ,"error": "POST request required."}, status=400)
    
    # get the new post content
    data = json.loads(request.body)
    post = Post.objects.get(pk=post_id)

    if request.user != post.poster:
        return JsonResponse({"result":"Failed" ,"error": "only posted User can edit the post"})
    
    post.content = data.get("content")
    post.save()

    return JsonResponse({"result":"Success", "action":"post update", "post":post.id}, status=201)


# View to toggle like/unlike of a post for request.user
@csrf_exempt
@login_required(login_url="/login")
def like_post(request, post_id):
    if request.method != "PUT":
        return JsonResponse({"result":"Failed" ,"error":"PUT request required"}, status=400)
    
    post = Post.objects.get(pk=post_id)
    data = json.loads(request.body)

    if data.get("like") == True:
        post.liked_users.add(request.user)
        return JsonResponse({"result":"Success", "action":"like", "post": post.id}, status=201)
    elif data.get("like") == False:
        post.liked_users.remove(request.user)
        return JsonResponse({"result":"Success", "action":"unlike", "post":post.id}, status=201)
    
    return JsonResponse({"result":"Failed" ,"error": "Invalid PUT request"}, status = 400)