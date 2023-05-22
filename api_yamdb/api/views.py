from django.db import IntegrityError
from django.db.models import Avg
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Categories, Comment, Genres, Review, Title
from users.models import User

from .filters import TitlesFilter
from .mixins import CDLViewSet, CRUDViewSet
from .utils import send_email
from .pagination import CategoriesPagination
from .permissions import IsAdminOrModeratorOrAuthor, IsAdminOrReadOnly
from .serializers import (CategoriesSerializer, CommentSerializer,
                          GenresSerializer, ReviewSerializer, SignUpSerializer,
                          TitlesRetrieveSerializer, TitlesWriteSerializer,
                          TokenSerializer, UserSerializer)


class UserViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(methods=['GET', 'PATCH'], detail=False,
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        user = self.request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(user, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        try:
            user, _create = User.objects.get_or_create(
                username=username,
                email=email
            )
        except IntegrityError:
            error = {}
            if User.objects.filter(email=email).exists():
                error['email'] = (
                    'Данный адрес электронной почты уже используется!')
            if User.objects.filter(username=username).exists():
                error['username'] = (
                    'Имя пользователя уже занято! Введите другое имя')
            return Response(error,
                            status=status.HTTP_400_BAD_REQUEST)
        send_email(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenView(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        user = User.objects.filter(username=username).first()
        if not user:
            return Response({'username': 'Неверное имя пользователя'},
                            status=status.HTTP_404_NOT_FOUND)
        confirmation_code = serializer.data['confirmation_code']
        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                {'confirmation_code': 'Неверный код подтверждения'},
                status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken.for_user(user)
        return Response(
            {'token': str(token.access_token)},
            status=status.HTTP_200_OK
        )


class CategoriesViewSet(CDLViewSet):

    queryset = Categories.objects.all().order_by('name')
    serializer_class = CategoriesSerializer
    pagination_class = CategoriesPagination

    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = "slug"


class GenresViewSet(CDLViewSet):

    queryset = Genres.objects.all().order_by('name')
    serializer_class = GenresSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

    pagination_class = CategoriesPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = "slug"


class TitlesViewSet(CRUDViewSet):
    """Вьюсет для произведения."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('name')
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    http_method_names = ("get", "post", "delete", "patch")

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitlesRetrieveSerializer
        return TitlesWriteSerializer


class ReviewViewSet(CRUDViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAdminOrModeratorOrAuthor,
        IsAuthenticatedOrReadOnly
    )
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            pk=self.kwargs['title_id']
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        IsAdminOrModeratorOrAuthor,
        IsAuthenticatedOrReadOnly
    )
    pagination_class = LimitOffsetPagination

    def object_review(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.object_review())
