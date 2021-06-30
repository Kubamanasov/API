from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import RegisterSerializer, ActivationSerializer, ForgotPasswordSerializer, \
    CreateNewPasswordSerializer,  LoginSerializer
# ChangePasswordSerializer,


class RegistrationView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Успешно зарегистрирован', status=status.HTTP_201_CREATED)


class ActivationView(APIView):

    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.activate()
            return Response('Ваш аккаунт успешно активирован!', status=status.HTTP_200_OK)


class LoginView(ObtainAuthToken):  # вход
    serializer_class = LoginSerializer


class LogoutView(APIView):  # выход

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response('Вы успешно вышли!')


class ResetPasswordView(APIView):  # запрос пароля
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_reset_email()
            return Response('Вам отправлен код для смены пароля', status=status.HTTP_200_OK)


class ResetPasswordCompleteView(APIView):

    def post(self, request):
        serializer = CreateNewPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.create_password()
            return Response('Пароль успешно обновлён', status=status.HTTP_200_OK)


# class ChangePasswordView(APIView):  # смена пароля
#
#     # permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         serializer = ChangePasswordSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.set_new_password()
#             return Response('Вы успешно поменяли пароль', status=status.HTTP_200_OK)
#
