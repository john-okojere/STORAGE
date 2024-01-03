from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from .manager import UserManager
from qrcode import *
import uuid


GENDER_CATEGORY=(
    ('Male','Male'),
    ('Female','Female'),
)
ROLE_CATEGORY=(
    ('ADMIN','ADMIN'),
    ('WRITER','WRITER'),
    ('USER','USER'),
)


class User(AbstractBaseUser, PermissionsMixin):
    uid = models.UUIDField( default=uuid.uuid4, editable=False)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        verbose_name='username',
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    first_name = models.CharField(verbose_name='first name', max_length=150, blank=True)
    last_name = models.CharField(verbose_name='last name', max_length=150, blank=True)
    phone_regex = RegexValidator(regex=r'^\+\d{8,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(
        validators=[phone_regex],
        max_length=16,
        unique=True,
        help_text="Phone number must be entered in the format: '+999999999'.",
        error_messages={
            'unique': "This Phone has been used already",
        },
        ) # validators should be a list
    email = models.EmailField(verbose_name='email address', unique=True,
        error_messages={
            'unique': "This email has been used already",
        },
    )
    gender = models.CharField(max_length= 20, choices=GENDER_CATEGORY)
    date_of_birth = models.DateField(null=True)
    role = models.CharField(max_length= 20, choices=ROLE_CATEGORY)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    update_fields = models.DateTimeField(auto_now=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone','email']


    objects = UserManager()
    
    def qr_code(self):
        qr_code = make(self.uid)
        basename = str(self.username) + '_QR_CODE.png'
        qr_code.save('media/QR_CODE/{}'.format(basename))
        return '/media/QR_CODE/{}'.format(basename)


    def save(self, *args, **kwargs):
        self.qr_code()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.last_name} {self.first_name} - {self.username}'

class About(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name="aboutprofile")
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    about = models.TextField()
    date_joined = models.DateTimeField(default=timezone.now)
    update_fields = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class ProfilePic(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name="profilepic")
    image = models.ImageField(upload_to="profile_pic/%y/%m/%d")
    date_joined = models.DateTimeField(default=timezone.now)
    update_fields = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
