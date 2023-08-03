from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
# Create your models here.

class User(AbstractUser):
    is_instructor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    email = models.EmailField(unique=True,)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',]
    
    def __str__(self):
        return self.username
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
    
    

class Instructor(models.Model):
    user = models.OneToOneField(User, related_name="instructor", on_delete=models.CASCADE)
    gender = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile-picture/')
    address = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return self.user.username

    
class Student(models.Model):
    user = models.OneToOneField(User, related_name="student", on_delete=models.CASCADE)
    gender = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile-picture/')
    address = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return self.user.username
    
    

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Accounteer"),
        # message:
        email_plaintext_message,
        # from:
        "support@accounteer.com",
        # to:
        [reset_password_token.user.email]
    )