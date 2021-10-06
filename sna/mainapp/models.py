from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Person(User):
    dob = models.DateField(null=True)
    accept = models.BooleanField(null=False, default=False)
    pic = models.ImageField(upload_to = "profilepic/%y", null = True)
    bio = models.CharField(max_length=200, null = True)
    city = models.CharField(max_length=70, null = True)
    country = models.CharField(max_length=70, null = True)
    profession = models.CharField(max_length=80, null = True)
    bgpic = models.ImageField(upload_to = "bg_pic/%y", null = True)
    followers = models.IntegerField(default=0)

class Post(models.Model):
    person = models.ForeignKey(Person, on_delete= models.CASCADE)
    time = models.DateTimeField()
    type = models.CharField(max_length=20)
    desc = models.CharField(max_length=150, null=True)
    video = models.FileField(upload_to= 'videos/%y', null=True)
    image = models.ImageField(upload_to= 'images/%y', null=True)
    text = models.TextField(max_length= 1500, null=True)
    likes = models.IntegerField(default=0)

class Liked(models.Model):
    person = models.ForeignKey(Person, on_delete= models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked = models.IntegerField()
    comment = models.CharField(max_length=500, null=True)

class Comment(models.Model):
    person = models.ForeignKey(Person, on_delete= models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=250)
    time = models.DateTimeField()

class Following(models.Model):
    follower = models.ForeignKey(Person, on_delete= models.CASCADE, related_name="follower")
    following = models.ForeignKey(Person, on_delete= models.CASCADE, related_name="following")

class Notification(models.Model):
    sender = models.ForeignKey(Person, on_delete= models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(Person, on_delete= models.CASCADE, related_name="receiver")
    read = models.BooleanField(default=False)
    message = models.CharField(max_length=100)
    time = models.DateTimeField()

    
