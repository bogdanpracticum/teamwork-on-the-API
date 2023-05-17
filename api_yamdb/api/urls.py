from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet,
    SignUpView,
    GetTokenView,
    GenresViewSet,
    CategoriesViewSet,
    TitlesViewSet,
    ReviewViewSet,
    CommentViewSet
)

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')
v1_router.register('categories', CategoriesViewSet, basename='categories')
v1_router.register('genres', GenresViewSet, basename='genres')
v1_router.register(r'genres/(?P<slug>[-\w]+)/$',
                   GenresViewSet, basename='genres_slug')
v1_router.register('titles', TitlesViewSet, basename='titles')
v1_router.register(r'titles/(?P<title_id>)/$',
                   TitlesViewSet, basename='titles_id')
v1_router.register(r'titles/(?P<title_id>[0-9]+)/reviews',
                   ReviewViewSet, basename='reviews')
v1_router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet,
    basename='comments'
)


urlpatterns = [
    path('v1/auth/token/', GetTokenView.as_view(), name='token'),
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/', include(v1_router.urls))]
