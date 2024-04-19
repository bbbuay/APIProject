from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import CartSerializer
from ..models import Cart 
from rest_framework.throttling import UserRateThrottle


class CartView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        carts = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        serializer = CartSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        user = request.user
        carts = Cart.objects.filter(user=user)
        carts.delete()
        return Response({"message": f"Successfully deleted all carts of user: {user.username}"}, status=status.HTTP_204_NO_CONTENT)


# class CartListCreateView(ListCreateAPIView):
#     queryset = Cart.objects.all()
#     permission_classes = [IsAuthenticated]
#     serializer_class = CartSerializer

#     def get_queryset(self):
#         return Cart.objects.filter(user=self.request.user)
    
# class CartDeleteView(DestroyAPIView):
#     queryset = Cart.objects.all()
#     permission_classes = [IsAuthenticated]
#     serializer_class = CartSerializer

#     def get_queryset(self):
#         return Cart.objects.filter(user=self.request.user)
    
#     def delete(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         breakpoint()
#         return super().delete(request, *args, **kwargs)
    