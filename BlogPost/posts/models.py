from django.db import models
#from ckeditor_uploader.fields import RichTextField
from Users.models import TopicTag,User,SubscribedUser

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=500, default="untitled")
    content = models.TextField(max_length=10000)
    tags = models.ManyToManyField(TopicTag, related_name='article_tags', blank=True) 
    published = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    def __str__(self):
        return str(self.title)
    
class Like(models.Model):
    user = models.ManyToManyField(User, related_name='liking_user')
    post = models.OneToOneField(Post, on_delete=models.CASCADE)

    @classmethod
    def like(cls, post, user):
        obj, create = cls.objects.get_or_create(post=post)
        obj.user.add(user)

    @classmethod
    def dislike(cls, post, user):
        obj, create = cls.objects.get_or_create(post=post)
        obj.user.remove(user)

    def __str__(self) -> str:
        return f'{self.post.title}'
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()


class SubComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
