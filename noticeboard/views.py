from django.shortcuts import render
from django.views import generic
from .models import Noticeboard, Comment, User

class NoticeboardListView(generic.ListView):
    model = Noticeboard
    template_name = 'noticeboardList.html'
    context_object_name = 'notices'
    
    
class NoticeboardDetailView(generic.DetailView):
    model = Noticeboard
    template_name = 'noticeboardDetail.html'
    context_object_name = 'notice'