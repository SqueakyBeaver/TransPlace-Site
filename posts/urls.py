from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import PostList, PostDetail, UserList, UserDetail

urlpatterns = [
    path("posts/", PostList.as_view(), name="api-posts"),
    path("posts/<str:pk>/", PostDetail.as_view()),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
