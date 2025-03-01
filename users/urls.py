from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('user', views.UserRetrieveView)
router.register('user-admin', views.UserAdminRetrieveListDestroyView)
router.register('profile', views.ProfileUpdateView)
router.register('wishlist', views.WishListView)

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]