from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate 
from .models import User, ProfilePic
from .forms import RegisterForm, EditRegisterForm

from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()


import random
def random_number():
    while True:
        i = random.randint(1,2)
        return i


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.role = "USER"
            form.save()
            username = request.POST.get('username')
            raw_password = request.POST.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user.gender == "Male":
                image = f"default/lg/male/avatar{random_number()}.jpg"
            elif user.gender == "Female":
                image = f"default/lg/female/avatar{random_number()}.jpg"
            propic = ProfilePic.objects.create(user=user, image=image)
            propic.save()
            login(request, user)
            messages.success(request, f"New account created: {username}")
            return redirect('profile', username=username)
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request, username):
    person = get_object_or_404(User, username=username)

    return render(request, 'users/index.html', {'person':person})

@login_required
def editprofile(request):
    if request.method == 'POST':
        form = EditRegisterForm(request.POST, instance = request.user)
        if form.is_valid():
            rform = form.save(commit=False)
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = EditRegisterForm( instance = request.user)
    return render(request, 'users/edit.html', {'form': form})

from .forms import ProfileForm
@login_required
def add_profilepic(request):
    if request.method == "POST":
        try:
            request.user.profilepic
            if request.user.profilepic:
                form =  ProfileForm(request.POST, request.FILES, instance=request.user.profilepic)
                if form.is_valid():
                    c_form = form.save(commit=False)
                    c_form.user = request.user
                    form.save()
        except:
            form =  ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                c_form = form.save(commit=False)
                c_form.user = request.user
                form.save()
    else:
        form =  ProfileForm()
    return redirect('profile', request.user.username)


from .forms import BioForm
from .models import About

@login_required
def addAbout(request):
    if request.method == "POST":
        form = BioForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = BioForm()
    return render(request, 'users/BioForm.html', {'form': form})


@login_required
def EditAbout(request):
    about = About.objects.get(user=request.user)
    if request.method == "POST":
        form = BioForm(request.POST, instance=about)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = BioForm(instance=about)
    return render(request, 'users/BioForm.html', {'form': form})
