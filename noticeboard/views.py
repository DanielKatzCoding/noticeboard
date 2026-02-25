from django.shortcuts import render
from django.views import generic
from .models import Noticeboard, Comment, User
from noticeboard import models
from django.db.models import Count

class NoticeboardListView(generic.ListView):
    model = Noticeboard
    template_name = 'noticeboardList.html'
    context_object_name = 'notices'
    
    def get_context_data(self, **kwargs):
        """Add comments count for each notice id to the context"""
        context = super().get_context_data(**kwargs)
        notices = context['notices']
        
        # Manually attach the count to each notice object in the list
        for notice in notices:
            notice.comments_count = Comment.objects.filter(noticeboard_id=notice.pk).count()
            
        return context
    
class NoticeboardDetailView(generic.DetailView):
    model = Noticeboard
    template_name = 'noticeboardDetail.html'
    context_object_name = 'notice'
    
    def get_context_data(self, **kwargs):
        """Add comments count for each notice id to the context"""
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(noticeboard_id=self.object.pk)
        
        return context
    