from home.models import Folder

def context(request):
    folders = Folder.objects.filter(folder=None).order_by('-date')
    context={
        'home_folders':folders
    }
    return context