from django.db import models
import uuid
from users import models as user_model



class Folder(models.Model):
    uid = models.UUIDField( default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    folder = models.ForeignKey('home.Folder',null=True, on_delete=models.CASCADE, related_name='parent')
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'

class File(models.Model):
    uid = models.UUIDField( default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    folder = models.ForeignKey('home.Folder',null=True, on_delete=models.CASCADE, related_name='_folder')
    file = models.FileField(upload_to="%y/%m/%d/")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.file}'
