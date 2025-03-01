from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout

from rest_framework import viewsets, mixins, permissions

from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.decorators import action

from .models import User, WishList
from .serializers import RegisterSerialzier, ProfileUpdateSerializer, UserSerializer, WishSerializer

class RegisterView(CreateModelMixin, GenericAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerialzier

class LoginView(APIView):
    def post(self, request):
        password = request.data.get('password')
        username = request.data.get('username')

        if not username or not password:
            return Response({'error': 'Please provide both username and password.'}, status=400)

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response({'message': 'Login successful.'}, status=200)
        else:
            return Response({'error': 'Invalid credentials.'}, status=401)
        
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful.'}, status=200)
    
#################################

# User Views
class UserRetrieveView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserAdminRetrieveListDestroyView(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class ProfileUpdateView(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileUpdateSerializer

    def get_object(self):
        return self.request.user


# Wishlist View
class WishListView(viewsets.GenericViewSet, 
                   mixins.CreateModelMixin, 
                   mixins.DestroyModelMixin, 
                   mixins.ListModelMixin, 
                   mixins.RetrieveModelMixin, 
                   mixins.UpdateModelMixin):
    queryset = WishList.objects.all()
    serializer_class = WishSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WishList.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_product_to_wishlist(self, request, pk):
        wishlist = self.get_object()
        product_id = request.data.get("product_id")

        if not product_id:
            return Response({'detail': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, pk=product_id)
        wishlist.product.add(product)

        serializer = self.get_serializer(wishlist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def remove_product_from_wishlist(self, request, pk):
        wishlist = self.get_object()
        product_id = request.data.get("product_id")

        if not product_id:
            return Response({'detail': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, pk=product_id)
        if product not in wishlist.product.all():
            return Response({'detail': 'Product is not in the wishlist.'}, status=status.HTTP_400_BAD_REQUEST)
        
        wishlist.product.remove(product)

        serializer = self.get_serializer(wishlist)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    


    

