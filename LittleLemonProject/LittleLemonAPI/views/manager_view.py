from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, Group
from ..serializers import UserListSerializer
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsManager
from django.shortcuts import get_object_or_404
from rest_framework.throttling import UserRateThrottle


class ManagerView(APIView):
    permission_classes = [IsAuthenticated, IsManager]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        managers = User.objects.filter(groups__name="Manager")
        serializer = UserListSerializer(managers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        username = request.data.get("username", "")
        if username:
            user = get_object_or_404(User, username=username)
            group = Group.objects.get(name="Manager")
            user.groups.add(group)
            return Response({"message": f"Successfully add `Manager` role to `{username}`"}, status=status.HTTP_201_CREATED)

        return Response({"message": "Please provided the user's username in playload"}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        group = Group.objects.get(name="Manager")
        user.groups.remove(group)
        return Response({"message": f"Successfully remove `Manager` role of UserID `{user.id}`"}, status=status.HTTP_201_CREATED)



