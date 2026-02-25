from django.urls import path
from .views import NoticeboardListView, NoticeboardDetailView, create_comment

app_name = 'noticeboard'
urlpatterns = [
    path('', NoticeboardListView.as_view(), name='noticeboard_list'),
    path('<int:pk>/', NoticeboardDetailView.as_view(), name='noticeboard_detail'),
    path('<int:pk>/comment/', create_comment, name='create_comment'),
]