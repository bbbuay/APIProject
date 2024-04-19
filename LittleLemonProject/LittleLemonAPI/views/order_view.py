from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ..serializers import OrderSerializer, UpdateOrderStatusSerializer
from ..models import Order, Cart, OrderItem
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.db import transaction
from ..permissions import IsCustomer, IsManager, IsDeliveryCrew, IsOderOwner
from rest_framework.throttling import UserRateThrottle

class OrderView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    ordering_fields=['user', 'date']
    search_fields = ['user__username', 'user__email', 'delivery_crew__username']
    throttle_classes = [UserRateThrottle]

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [IsAuthenticated]
        else: # POST
            permission_classes = [IsAuthenticated, IsCustomer]
        return [permission() for permission in permission_classes]


    def get_queryset(self):
        user = self.request.user 
        # manager
        if user.groups.filter(name="Manager"):
            return self.queryset.all()
        
        # delivery crew
        if user.groups.filter(name="Delivery crew"):
            return self.queryset.filter(delivery_crew=user)
        
        # customer
        return self.queryset.filter(user=user)

    
    def perform_create(self, serializer):
        with transaction.atomic():
            order = serializer.save(user=self.request.user)

            # Gets current cart items and adds those items to the order items table. 
            # Then deletes all items from the cart for this user.
            carts = Cart.objects.filter(user=self.request.user)
            for c in carts:
                OrderItem.objects.create(
                    order=order,
                    menuitem=c.menuitem,
                    quantity=c.quantity,
                    unit_price=c.unit_price,
                    price=c.price
                )
            carts.delete()
        
class OrderSingleView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # def get_serializer(self, *args, **kwargs):
    #     return super().get_serializer(*args, **kwargs)
    
    def get_serializer_class(self):
        if self.request.method == "PATCH" and self.request.user.groups.filter(name="Delivery crew"): 
            return UpdateOrderStatusSerializer     
        return self.serializer_class
    
    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [IsAuthenticated, IsOderOwner]
        if self.request.method == "PUT" or self.request.method == "PATCH":
            permission_classes = [IsAuthenticated & (IsManager | IsDeliveryCrew)]
        if self.request.method == "DELETE":
            permission_classes = [IsAuthenticated, IsManager]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user 

        # manager
        if user.groups.filter(name="Manager"):
            return self.queryset.all()
        
        # delivery crew
        if user.groups.filter(name="Delivery crew"):
            return self.queryset.filter(delivery_crew=user)
        
        # customer
        return self.queryset.filter(user=user)


    
    


    