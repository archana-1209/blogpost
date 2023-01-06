from rest_framework.permissions import IsAuthenticated
from .models import  TopicTag
from posts.serializers import PostSerializer,CommentSerializer,SubcomentSerializer
from rest_framework import viewsets
from rest_framework import viewsets, authentication, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from Users.models import SubscribedUser
from posts.models import Post
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission
from .models import Like,Comment,SubComment
from django.http import JsonResponse, HttpResponseForbidden

# def is_subscribed(user):
#     """
#     Allows access only to "subscribed" users.
#     """
    
   

class PostsViewset(viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class=PostSerializer
    
    def get_queryset(self):
        #user=self.request.user
        #subscribed_user=SubscribedUser.objects.filter(user=user).first()
        queryset=Post.objects.all()
        return queryset
        
        
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=["post"])
    def like_dislike_post(self,request,pk=None):
        post = Post.objects.get(id=pk)
        
        user =request.user
        is_liked = False
        if Like.objects.filter(user=user, post=post).exists():
            Like.dislike(user=user, post=post)
        else:
            Like.like(user=user, post=post)
            is_liked = True
            

        like_obj = Like.objects.get(post=post)
        total_likes = like_obj.user.count()
        post.likes = total_likes
        post.save()
        return JsonResponse({'is_liked': is_liked, 'total_likes': total_likes})

    @action(detail=True,methods=["post","get"])
    def comment(self,request,pk=None):
        comm = request.data.get('comm',None)
        comm_id=request.data.get('comm_id',None)
        user=request.user
        post=Post.objects.get(id=pk)
        if request.method=="POST":
            if comm_id:
                comment=Comment.objects.get(id=comm_id)
                data={}
                data["post"]=post.id
                data["user"]=user.id
                data["message"]=comm
                data["comment"]=comment.id
                print(data)
                serializer=SubcomentSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.create(serializer.validated_data)
                response=serializer.validated_data
                print(response)
                
            
                comment = Comment.objects.get(id=comm_id)
                
            else:
                data={}
                data["post"]=post.id
                data["user"]=user.id
                data["message"]=comm
                serializer=CommentSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.create(serializer.validated_data)
                
                post.comments += 1
                post.save()
            comments = []
        
        response={}
        for comment in Comment.objects.filter(post=post):
            comment_id=CommentSerializer(comment).data.get('id')
            comments=SubComment.objects.filter(comment=comment)
            if comment_id in response.keys():
                response[comment_id]+=SubcomentSerializer(comments,many=True).data
            else:
                response[comment_id]=SubcomentSerializer(comments,many=True).data
           
            
        return JsonResponse(response)
        