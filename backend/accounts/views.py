from django.conf import settings
from django.core.mail import send_mail
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer
import jwt


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def user_view(request, pk):
    if request.method == 'POST':
        serializer_user = UserSerializer(data=request.data)
        if serializer_user.is_valid():
            user = serializer_user.save()
            user.set_password(request.data['password'])
            return Response(serializer_user.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_user.errors, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer_user = UserSerializer(user)
        return Response(serializer_user.data, status=status.HTTP_202_ACCEPTED)
    elif request.method == 'PUT':
        serializer_user = UserSerializer(user, data=request.data)
        if serializer_user.is_valid():
            serializer_user.save()
            return Response(serializer_user.data)
        return Response(serializer_user.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def account_view(request):
    if request.method == 'GET':
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
            return Response(status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        password = request.data['password']
        serializer_user = UserSerializer(data=request.data)
        if serializer_user.is_valid():
            user = serializer_user.save()
            user.set_password(password)
            user.save()
            send_mail(subject='Подтверждение аккаунта!',
                      message=f"Перейдите по ссылке чтобы активировать аккаунт: http://localhost:3000/activate/?token={RefreshToken.for_user(user=user)}",
                      from_email='practika.test2@gmail.com',
                      recipient_list=[request.data['email']],
                      fail_silently=True, )
            return Response(serializer_user.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_user.errors, status=status.HTTP_400_BAD_REQUEST)
