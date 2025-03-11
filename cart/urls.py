from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'user-cart-view', views.UserCartView)
router.register(r'user-cart-update', views.UserAddRemoveItemToCartView)
router.register(r'admin-cart-view', views.AdminCartView)


urlpatterns = [
    path('', include(router.urls)),
]