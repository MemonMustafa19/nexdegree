from rest_framework import generics, status, mixins
from rest_framework.response import Response
from .models import User
from .serializers import *
from rest_framework.permissions import AllowAny
from django.db.models import F, Q

# Create your views here.

class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "Registered successfully!",
        }, status=status.HTTP_201_CREATED)


class UserCRUD(generics.GenericAPIView, mixins.ListModelMixin,
               mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
               mixins.DestroyModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

    def get(self, request, id=None):

        if id:
            return self.retrieve(request)

        else:
            return self.list(request)

    def put(self, request, id=None):
        if 'password' in request.data:
            return Response({"password": "Password can only be changed using the change-password route."}, status=status.HTTP_400_BAD_REQUEST)
        return self.update(request, id, partial=True)

    def delete(self, request, id):
        return self.destroy(request, id)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully!',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Successfully logged out!"}, status=status.HTTP_204_NO_CONTENT)
