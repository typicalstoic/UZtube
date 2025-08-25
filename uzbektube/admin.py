from django.contrib import admin
from .models import Category, VideoContent, Comment, Profile, Ip

admin.site.register(Category)
admin.site.register(VideoContent)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Ip)
