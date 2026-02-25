from tokenize import Comment

from django.contrib import admin

from .models import Noticeboard, User, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Noticeboard)
admin.site.register(Comment)