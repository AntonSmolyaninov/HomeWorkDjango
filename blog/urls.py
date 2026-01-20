from django.urls import path
from .views import (
    BlogPostListView,
    BlogPostDetailView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView,
)

app_name = 'blog'

urlpatterns = [
    path('', BlogPostListView.as_view(), name='post_list'),  # список постов
    path('post/create/', BlogPostCreateView.as_view(), name='post_create'),  # -> сюда вверх!
    path('post/<int:pk>/', BlogPostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', BlogPostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='post_delete'),
]
