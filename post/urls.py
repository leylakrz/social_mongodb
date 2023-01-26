from django.urls import path
from rest_framework.routers import DefaultRouter

from post.views import PostViewSet, PostApiView, LikeViewSet, CommentViewSet

post_router = DefaultRouter()
post_router.register('', PostViewSet, basename='post')
post_router.register('', LikeViewSet, basename='like')
post_router.register('', CommentViewSet, basename='comment')

urlpatterns = [
                  path("<str:user_name>/", PostApiView.as_view())
              ] + post_router.urls
