from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from . import forms
from .models import Folder, File
from django.conf import settings
import os
from django.db.models import Q


def homepage(request):
    folders = Folder.objects.filter(folder=None).order_by('-date')
    return render(request, 'home/index.html', {'folders':folders})

@login_required
def AddFolder(request):
    if request.method =="POST":
        form = forms.FolderForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            form.save()
            return redirect('/')
    else:
        form = forms.FolderForm()
    return render(request, 'form/index.html', {'form':form})

def get_parent_hierarchy(folder):
    parent_hierarchy = []
    
    while folder.folder:
        parent_hierarchy.insert(0, folder.folder)
        folder = folder.folder

    return parent_hierarchy

def ViewFolder(request, uid):
    folder = Folder.objects.get(uid=uid)
    folders = Folder.objects.filter(folder=folder)
    files = File.objects.filter(folder=folder)

    context = {
       'parent_hierarchy': get_parent_hierarchy(folder),
        'folder': folder,
        'files': files,
        'folders': folders,
    }
    return render(request, 'home/folder.html', context)

@login_required
def AddSubFolder(request, uid):
    folder = Folder.objects.get(uid=uid)
    if request.method =="POST":
        form = forms.FolderForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.folder = folder
            form.save()
            return redirect('folder', uid= folder.uid)
    else:
        form = forms.FolderForm()
    return render(request, 'form/index.html', {'form':form,'folder':folder})


def get_subfolders_json(request, uid):
    folder = Folder.objects.get(uid=uid)
    subfolders = Folder.objects.filter(folder=folder).order_by('-date')

    subfolders_data = [{'uid': subfolder.uid, 'name': subfolder.name} for subfolder in subfolders]

    return JsonResponse({'subfolders': subfolders_data})


@login_required
def AddFile(request, uid):
    folder = Folder.objects.get(uid=uid)
    if request.method =="POST":
        form = forms.FileForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        if form.is_valid():
            for uploaded_file in files:
                f = File(user=request.user, file=uploaded_file, folder=folder)
                f.save()
            return redirect('folder', uid= folder.uid)
    else:
        form = forms.FileForm()
    return render(request, 'form/file.html', {'form':form, 'folder':folder})

def format_file_size(file_size):
    size_suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    i = 0
    while file_size >= 1024 and i < len(size_suffixes)-1:
        file_size /= 1024.0
        i += 1

    return f"{file_size:.2f} {size_suffixes[i]}"

@login_required
def viewFile(request, uid):
    file = File.objects.get(uid=uid)
    file_path = os.path.join(settings.MEDIA_ROOT, str(file.file))
    file_size = os.path.getsize(file_path)
    file.size = format_file_size(file_size)
    context ={
        'file':file,
        'parent_hierarchy': get_parent_hierarchy(file.folder),
    }
    return render(request, 'home/file.html', context)

@login_required
def recentfile(request):
    files = File.objects.all().order_by('-date')[:30]
    context ={
        'files':files,
    } 
    return render(request, 'home/recent.html', context)


@login_required
def recentfolder(request):
    folder = Folder.objects.all().order_by('-date')[:30]
    context ={
        'folders':folder,
    } 
    return render(request, 'home/recent.html', context)


def search(request):
    query = request.GET.get('q','')
    results = []

    if query:
        # Perform a search across multiple models and fields
        folder = Folder.objects.filter(Q(name__icontains=query))
        file = File.objects.filter(Q(file__icontains=query))
        # Number of items to show per page
    context = {'query': query, 'files':file ,'folders':folder}
    return render(request, 'home/recent.html', context)