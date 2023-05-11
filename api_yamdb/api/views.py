
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.http import Http404

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from .serializers import (
    UserSerializer, SignUpSerializer, TokenSerializer)

from reviews.models import User
from api_yamdb.settings import ADMIN_EMAIL


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


def send_email(user):
    confirmation_code = default_token_generator.make_token(user)
    email_subject = 'Код для авторизации'
    email_text = f'Ваш код для авторизации - {confirmation_code}'
    admin_email = ADMIN_EMAIL
    user_email = [user.email]
    return send_mail(email_subject, email_text, admin_email, user_email)


class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        try:
            user, create = User.objects.get_or_create(
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
        try:
            user = get_object_or_404(User, username=username)
        except Http404:
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

