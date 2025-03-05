from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.generics import ListAPIView
from rest_framework.decorators import action
from .models import Product, Category, Review
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer


class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["price", "stock_quantity", "is_active", "average_rating"]
    
class ProductCategoryView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs["category_slug"])
        return Product.objects.filter(category=category) 
           
#####################

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class= CategorySerializer

#####################

class ReviewView(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product = get_object_or_404(Product, sku=self.kwargs["product_sku"])
        return Review.objects.filter(product=product, status="approved")


class AdminReviewView(viewsets.ModelViewSet, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True, methods=["patch"])
    def approve_review(self, request, pk=None):
        review = self.get_object()  
        
        review.approve()

        return Response({'status': 'approved'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["patch"])
    def reject_review(self, request, pk=None):
        review = self.get_object()  
        
        review.reject()

        return Response({'status': 'rejected'}, status=status.HTTP_200_OK)

class UserReviewView(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["product"]
    
    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
        
class UserReviewProductView(ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        product = get_object_or_404(Product, sku=self.kwargs["product_sku"])
        return Review.objects.filter(user=self.request.user, product=product)
    
#####################

