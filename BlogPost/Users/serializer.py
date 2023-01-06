from rest_framework import serializers
from django.contrib.auth.models import User
from email_validator import validate_email, EmailNotValidError
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

from .models import UserProfile, TopicTag, SkillTag


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    ) 
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'is_superuser', 'is_staff','password']
        
    def validate_email(self,value):
        try:
            validated_email_data =validate_email(value)
            email_add = validated_email_data['email']
            return email_add
        except EmailNotValidError as e:
            raise serializers.ValidationError(str(e))







class TopicTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicTag
        fields = '__all__'

class SkillTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillTag
        fields = '__all__'


# class UserProfileUpdateSerializer(serializers.ModelSerializer):
#     interests = TopicTagSerializer(many=True, read_only=True)
#     skills = SkillTagSerializer(many=True, read_only=True)
#     class Meta:
#         model = UserProfile
#         fields = '__all__'

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    interests = TopicTagSerializer(many=True, read_only=True)
    skills = SkillTagSerializer(many=True, read_only=True)
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    interests = TopicTagSerializer(many=True, read_only=True)
    skills = SkillTagSerializer(many=True, read_only=True)
    class Meta:
        model = UserProfile
        fields = '__all__'

class ListUserProfileSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=UserProfile
        fields='__all__'
        
    def get_user(self,obj):
        data={}
        user=obj.user
        data['email']=user.email
        return data
        
class CurrentUserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id','profile', 'username','email','is_superuser', 'is_staff']

    def get_profile(self, obj):
        print("object1",obj)
        
        profile = obj.userprofile
        serializer = UserProfileSerializer(profile, many=False)
        return serializer.data

class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'profile', 'username', 'is_superuser', 'is_staff']

    def get_profile(self, obj):
        profile = obj.userprofile
        serializer = UserProfileSerializer(profile, many=False)
        return serializer.data


