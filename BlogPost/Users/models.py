

from django.contrib.auth.models import User,AbstractBaseUser
from django.db import models
import uuid
from django.contrib.auth.models import PermissionsMixin


class TopicTag(models.Model):
    name = models.CharField(primary_key=True, max_length=150, null=False, blank=False)

    def __str__(self):
        return self.name



class SkillTag(models.Model):
    name = models.CharField(primary_key=True, max_length=150, null=False, blank=False)

    def __str__(self):
        return self.name

# class User(AbstractBaseUser, PermissionsMixin):
#     has_subscription=models.BooleanField(default=False)
    
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers_count = models.IntegerField(blank=True, null=True, default=0)
    skills = models.ManyToManyField(SkillTag, related_name='personal_skills', blank=True)
    interests = models.ManyToManyField(TopicTag, related_name='topic_interests', blank=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
   
    @classmethod
    def unfollow(cls, userprofile_to_follow, user):
        userprofile_to_follow.followers.remove(user)
        userprofile_to_follow.followers_count = userprofile_to_follow.followers.count()-1
        userprofile_to_follow.save()
       
    @classmethod
    def follow(cls, userprofile_to_follow, user):
        print(cls)
        userprofile_to_follow.followers.add(user)
        userprofile_to_follow.followers_count = userprofile_to_follow.followers.count()+1
        userprofile_to_follow.save()

    def __str__(self):
        return str(self.user.username)
    
class SubscribedUser(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    no_of_posts=models.IntegerField(default=0)
    is_active=models.BooleanField(default=False)
    posts_views=models.IntegerField(default=0)
    
    
     