from rest_framework import routers

from Users.viewsets import UserProfileViewset
from posts.viewsets import PostsViewset
router = routers.DefaultRouter()

# Project router
router.register('user-profiles', UserProfileViewset, basename='user-profiles')
router.register('posts',PostsViewset,basename='posts')