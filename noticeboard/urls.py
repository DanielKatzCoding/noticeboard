from django.urls import path
from .views import NoticeboardListView, NoticeboardDetailView

urlpatterns = [
    path('', NoticeboardListView.as_view(), name='noticeboard_list'),
    path('<int:pk>/', NoticeboardDetailView.as_view(), name='noticeboard_detail'),
]