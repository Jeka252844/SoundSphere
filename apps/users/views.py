from rest_framework.generics import (ListAPIView, CreateAPIView, GenericAPIView, 
    UpdateAPIView, DestroyAPIView, RetrieveAPIView)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users.models import User
from apps.users.permissions import IsAdmin, IsModerator, IsOwner
from apps.users.user_serializer import (UserSerializer, UserCreateSerializer,
 UserUpdateSerializer, UserPasswordSerializer)

class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsModerator, )

class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny, )

class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwner | IsModerator, )

class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = (IsOwner, )

    def get_object(self):
        user = self.request.user
        return User.objects.get(id = user.id)

class UserPasswordUpdateAPIView(GenericAPIView):
    serializer_class = UserPasswordSerializer
    permission_classes = (IsOwner, )

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)

        old = serializer.validated_data['old_password']
        new = serializer.validated_data['new_password']
        
        if old == new:
            return Response({'error': 'Новый пароль должен отличаться от старого'}, status=400)

        user = request.user
        if not user.check_password(old):
            return Response({'error': 'Неверный старый пороль'}, status=400)
        
        user.set_password(new)
        user.save()
        return Response({'success': True})

class UserDeleteAPIView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = (IsOwner | IsAdmin, )