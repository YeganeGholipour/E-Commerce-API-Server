from rest_framework.response import Response
from rest_framework import status, permissions, mixins, viewsets
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartItemSerializer, CartSerializer

class UserCartView(viewsets.GenericViewSet, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart
    

class UserAddRemoveItemToCartView(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}
    
    def get_object(self):
        return get_object_or_404(CartItem, pk=self.kwargs["pk"], cart=self.request.user.cart)


class AdminCartView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    permission_classes = [permissions.IsAdminUser]
