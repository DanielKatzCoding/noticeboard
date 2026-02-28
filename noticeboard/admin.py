from django.contrib import admin

from .models import Comment, Noticeboard, User

# Register your models here.
admin.site.register(User)
admin.site.register(Noticeboard)
admin.site.register(Comment)
