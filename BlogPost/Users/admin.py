from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import (
    SkillTag, TopicTag, UserProfile
)

# Register your models here.
admin.site.register(SkillTag)
admin.site.register(TopicTag)
admin.site.register(UserProfile)
