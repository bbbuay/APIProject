from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from ..serializers import MenuItemSerializer
from ..models import MenuItem
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsManager
from rest_framework.throttling import UserRateThrottle


# Create your views here.
class MenuItemView(ListCreateAPIView):
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()
    ordering_fields=['title', 'price', 'category__title']
    search_fields = ['title', 'category__title']
    throttle_classes = [UserRateThrottle]

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsManager]
        return [permission() for permission in permission_classes]
    

class MenuItemSingleView(RetrieveUpdateDestroyAPIView):
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsManager]
        return [permission() for permission in permission_classes]
