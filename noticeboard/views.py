from django.shortcuts import redirect, render
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
    
def create_comment(request, pk):
    if request.method == 'POST':
        content: str = request.POST.get('content')
        author: str = request.POST.get('author').lower().capitalize()
        
        notice = Noticeboard.objects.filter(pk=pk).first()
        user = User.objects.filter(username=author).first()
        if not user:
            user = User.objects.create(username=author)
            
        Comment.objects.create(noticeboard=notice, content=content, author=user)
    return redirect('noticeboard:noticeboard_detail', pk=pk)
    
def create_notice(request):
    if request.method == 'POST':
        content: str = request.POST.get('content')
        title: str = request.POST.get('title')
        author: str = request.POST.get('author').lower().capitalize()
        
        user = User.objects.filter(username=author).first()
        if not user:
            user = User.objects.create(username=author)
            
        Noticeboard.objects.create(title=title, content=content, author=user)
        return redirect('noticeboard:noticeboard_list')
    return render(request, 'noticeForm.html')
    