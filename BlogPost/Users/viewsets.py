from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, SkillTag, TopicTag
from .serializer import (UserProfileSerializer,CurrentUserSerializer,ListUserProfileSerializer,UserProfileUpdateSerializer)
from rest_framework import viewsets
from rest_framework import viewsets, authentication, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

class UserProfileViewset(viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
     
    
       
    serializer_class=UserProfileSerializer
    action_serializers = {
       
        'list': ListUserProfileSerializer,
        'retrieve': UserProfileSerializer,
        'partial_update':UserProfileUpdateSerializer
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]

        return super(UserProfileViewset, self).get_serializer_class()


    def get_queryset(self):
        queryset= UserProfile.objects.all()
        skill=self.request.query_params.get("skill", None)
        if skill:
            queryset=queryset.filter(skills__in=[skill])
            
        
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        
        user = request.user
        user_profile=UserProfile.objects.filter(user=user).first()
        skills = request.data.get('skills',None)
        interests=request.data.get('interests',None)
        if skills:
            user_profile.skills.set(
                SkillTag.objects.get_or_create(name=skill)[0] for skill in skills
            )
           
        if interests:
            user_profile.interests.set(
            TopicTag.objects.get_or_create(name=interest)[0] for interest in interests
            )
        user_profile.save()
        serializer = UserProfileUpdateSerializer(user_profile)
        return Response(serializer.data)
           
            

        #return super().partial_update(request, *args, **kwargs)
        
        
    @action(detail=False, methods=["POST"])
    def follow_user(self,request):
        requested_user = self.request.user
        username=request.data.get('username',None)
        if username:
            user = User.objects.filter(username=username).first()
            userprofile=UserProfile.objects.filter(user=user).first()
            if requested_user == user:
                return Response('You can not follow yourself')
            if requested_user in userprofile.followers.all():
                UserProfile.unfollow(userprofile_to_follow=userprofile,user=requested_user)  
                message=f"{requested_user.username} unfollowed ."
                return Response(message)
            else:
                UserProfile.follow(userprofile_to_follow=userprofile,user=requested_user)   
                message=f"{requested_user.username} started following you."
                return Response(message)
        else:
            message="error"
            return Response(message,status=status.HTTP_204_NO_CONTENT)
