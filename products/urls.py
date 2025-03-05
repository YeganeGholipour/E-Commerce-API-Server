from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductView)
router.register(r'categories', views.CategoryView)
router.register(r'reviews', views.ReviewView)
router.register(r'admin-review', views.AdminReviewView)
router.register(r'user-review', views.UserReviewView)

urlpatterns = [
    path('', include(router.urls)),
    path('user-review/<str:product_sku>/', views.UserReviewProductView.as_view(), name='user-reviews-for-product'),
    path('categories/<slug:category_slug>/products/', views.ProductCategoryView.as_view(), name='products-by-category'),
]