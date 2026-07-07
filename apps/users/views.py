from rest_framework.generics import (ListAPIView, CreateAPIView, GenericAPIView, 
                                    UpdateAPIView, DestroyAPIView, RetrieveAPIView)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.models import User
from users.user_serializer import (UserSerializer, UserCreateSerializer,
 UserUpdateSerializer, UserPasswordSerializer, UserTokenObtainSerializer)

class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny, )

class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = (AllowAny, )

    def get_object(self):
        user = self.request.user
        return User.objects.get(id = user.id)

class UserPasswordUpdateAPIView(GenericAPIView):
    serializer_class = UserPasswordSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.get_serializer(data=request)
        serializer.is_valid(raise_exception = True)

        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'error': 'Неверный старый пороль'}, status=400)
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'success': True})

class UserDeleteAPIView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny, )

class UserTokenObtainPairView(TokenObtainPairView):
    pass
