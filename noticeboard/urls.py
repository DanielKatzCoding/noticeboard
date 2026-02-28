from django.urls import path

from .views import (
    NoticeboardDetailView,
    NoticeboardListView,
    create_comment,
    create_notice,
)

app_name = 'noticeboard'
urlpatterns = [
    path('', NoticeboardListView.as_view(), name='noticeboard_list'),
    path('<int:pk>/', NoticeboardDetailView.as_view(), name='noticeboard_detail'),
    path('<int:pk>/comment/', create_comment, name='create_comment'),
    path('create/', create_notice, name='create_notice'),
]
