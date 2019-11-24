from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate, get_user
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from django.db import IntegrityError
from .models import Item
import os

def index(request):
    if get_user(request):
        return redirect("/self/"+str(get_user(request)))
    else:
        return redirect("/login")

def search(request):
    if request.method == "POST":
        users = User.objects.filter(username__icontains = request.POST['search'])
        return render(request, "search.html", {"result": users})
    else:
        return render(request, "search.html", {})

@login_required(login_url="/login")
def self(request, name):
    if get_user(request).username != name:
        items = Item.objects.filter(author__username = name, access = True).order_by("-id")
        return render(request, "self.html", {"item": items, "who": name})
    else:
        items = Item.objects.filter(author__username = name).order_by("-id")
        return render(request, "self.html", {"item": items, "who": name})

@login_required(login_url ="/login")
def upload(request, name):
    if name != get_user(request).username:
        return redirect('/self/'+str(get_user(request))+"/upload")
    if request.method == "POST":
        try:
            access = False
            if request.POST["access"] == "General":
                access = True
            elif request.POST["access"] == "Private":
                access = False
            Item.objects.create(author = get_user(request), File = request.FILES["file"], access = access)
            return redirect("/self/"+str(name)+"/")
        except MultiValueDictKeyError:
            return redirect("/self/"+str(name)+"/upload")
    else:
        return render(request, "upload.html", {})

@login_required(login_url = "/login")
def delete(request, name, id):
    if name == get_user(request).username:
        item = Item.objects.get(author__username = name, id = id)
        os.remove(str(item.File.path))
        item.delete()
        return redirect("/self/"+str(name))
    else:
        return redirect("/self/"+str(name))

def loginn(request):
    if request.method == 'POST':
        try:
            user = authenticate(username = request.POST["username"], password = request.POST["password"])
            login(request, user)
            return redirect("/self/"+str(request.POST["username"]))
        except AttributeError:
            return redirect("/signup")
    else:
        return render(request, "login.html", {})

def signup(request):
    if request.method == "POST":
        if request.POST["username"] == "" or request.POST['password'] == '':
            return redirect("/signup")
        else:
            try:
                user = User.objects.create_user(username = request.POST["username"], password = request.POST["password"])
                user.save()
                return redirect("/login")
            except IntegrityError:
                return redirect("/signup")
    else:
        return render(request, "signup.html", {})

@login_required(login_url = "/login")
def logoutt(request):
    logout(request)
    return redirect("/")