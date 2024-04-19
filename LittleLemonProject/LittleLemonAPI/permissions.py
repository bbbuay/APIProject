from rest_framework import permissions
from .models import Order
from django.shortcuts import get_object_or_404



class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Manager").exists()
    
class IsDeliveryCrew(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Delivery crew").exists()

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        # customer should not belong to any groups
        return not request.user.groups.all().exists()
    
class IsOderOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        order_id = request.parser_context["kwargs"]["pk"]
        order = get_object_or_404(Order, pk=order_id)
        return order.user == request.user