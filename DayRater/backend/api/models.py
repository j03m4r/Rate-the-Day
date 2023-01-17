from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    date = models.DateField(auto_now=True)
    text = models.TextField(max_length=100)
    
class DayRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    date = models.DateField(auto_now=True)
    rating = models.IntegerField(default=0)
    description = models.TextField(max_length=200)
    likes = models.ManyToManyField(User, related_name='rating')
    comments = models.ManyToManyField(Comment, related_name='rating')
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    bio = models.TextField(max_length=1000)
    followers = models.ManyToManyField(User, related_name="following")
    following = models.ManyToManyField(User, related_name="followers")
    ratings = models.ManyToManyField(DayRating, related_name="profile")