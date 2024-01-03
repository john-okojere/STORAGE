from django import forms
from . import models


class FolderForm(forms.ModelForm):
    class Meta:
        model = models.Folder
        fields = ('name',)

class FileForm(forms.ModelForm):
    class Meta:
        model = models.File
        fields = ('file',)