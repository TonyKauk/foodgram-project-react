# from django.urls import include, path
# from rest_framework.routers import DefaultRouter
# 
# from .views import (
#     CategoryViewSet, CommentViewSet, GenreViewSet,
#     ReviewViewSet, SingupViewSet, TitleViewSet,
#     TokenViewSet, UserViewSet
# )
# 
# router = DefaultRouter()
# router_auth = DefaultRouter()
# 
# router_auth.register(
#     'token', TokenViewSet, basename='tokens'
# )
# router_auth.register(
#     'signup', SingupViewSet, basename='signups'
# )
# 
# router.register(
#     'users', UserViewSet, basename='users'
# )
# router.register(
#     r'categories', CategoryViewSet, basename='categories'
# )
# router.register(
#     r'genres', GenreViewSet, basename='genres'
# )
# router.register(
#     r'titles', TitleViewSet, basename='titles'
# )
# router.register(
#     r'titles/(?P<title_id>\d+)/reviews',
#     ReviewViewSet,
#     basename='reviews',
# )
# router.register(
#     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     CommentViewSet,
#     basename='comments',
# )
# 
# 
# urlpatterns = [
#     path('v1/', include(router.urls)),
#     path('v1/auth/', include(router_auth.urls)),
# ]