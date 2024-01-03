from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('addFolder/', views.AddFolder, name='addfolder'),
    path('Search/', views.search, name='search'),
    path('RecentFile/', views.recentfile, name='recentfile'),
    path('RecentFolder/', views.recentfolder, name='recentfolder'),

    path('addSubFolder/<uuid:uid>', views.AddSubFolder, name='addSubfolder'),
    path('addFile/<uuid:uid>', views.AddFile, name='addFile'),
    path('File/<uuid:uid>', views.viewFile, name='File'),
    path('Folder/<uuid:uid>', views.ViewFolder, name='folder'),

    path('getFolder/<uuid:uid>', views.get_subfolders_json, name='getfolder'),
]

