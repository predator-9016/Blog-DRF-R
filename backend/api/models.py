from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
import shortuuid
# Create your models here.


#! creating the user
class User(AbstractUser):
    username = models.CharField(unique=True,max_length=100)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, null=True,blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def save(self,*args,**kwargs):
        # self.username = slugify(self.email)
        email_username , mobile = self.email.split("@")
        if self.full_name == "" or self.full_name == None:
            self.full_name = email_username
        if self.username == "" or self.username == None:
            self.username = email_username

        super(User , self).save(*args,**kwargs)


#profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to="image",default="default/default-user.jpg",null=True,blank=True)
    full_name = models.CharField(max_length=100 , null=True , blank=True)
    bio = models.CharField(max_length=100 , null=True , blank=True)
    about = models.CharField(max_length=100 , null=True , blank=True)
    author = models.BooleanField(default=False)
    country = models.CharField(max_length=100, null=True, blank=True)
    facebook = models.CharField(max_length=100, null=True, blank=True)
    twitter = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return self.user.username
    class Meta:
        ordering =['user']

    def save(self,*args,**kwargs):
        short = self.user
        if self.full_name == "" or self.full_name == None:
            self.full_name = short.full_name
        # if self.full_name == "" or self.full_name == None:
        #     self.full_name = self.user.full_name


        super(Profile , self).save(*args,**kwargs)

def create_user_profile(sender , instance ,created ,**kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender , instance , **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile , sender=User)
post_save.connect(save_user_profile , sender=User)


class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to="image", null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)


    def __str__(self):
        return self.title
    
    class Meta:
        ordering =['title']

    def save(self , *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.title)
            super(Category , self).save(*args,**kwargs)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)