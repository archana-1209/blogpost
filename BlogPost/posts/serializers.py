from rest_framework import serializers
from posts.models import Post,Comment,SubComment

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields='__all__'
        
class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Comment
        fields='__all__'
        
class SubcomentSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubComment
        fields='__all__'
# class absseriaizer(serializers.ModelSerializer):
#     sucomment = SubcomentSerializer(many=True)
#     class Meta:
#         model=SubComment
#         fields=['sucomment']