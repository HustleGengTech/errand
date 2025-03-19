from django.contrib import admin
from .models import Profile, Post, Comment,LikedPost,Review
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(LikedPost)
admin.site.register(Review)
