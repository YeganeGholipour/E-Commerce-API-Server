from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from .serializers import OrderSerializer, ShippingSerializer
from .models import Order, Shipping

class UserOrderView(GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()  

    def get_queryset(self):
        return Order.objects.filter(cart__user=self.request.user)
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = super().get_object()
        if obj not in queryset:
            raise PermissionDenied("You do not have permission to view this order.")
        return obj
    
    @action(detail=True, methods=['post'])
    def successful_payment(self, request, *args, **kwargs):
        order = self.get_object()
        order.payment_status = 'Paid'
        order.save()
        return Response({'message': 'Payment successful.'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def cancel_payment(self, request, *args, **kwargs):
        order = self.get_object()
        order.payment_status = 'Cancelled'
        order.save()
        return Response({'message': 'Payment cancelled.'}, status=status.HTTP_200_OK)


class AdminOrderView(GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True, methods=['post'])
    def ship_delivery(self, request, *args, **kwargs):
        order = self.get_object()
        
        if order.payment_status != 'Paid':
            return Response({'message': 'Payment not successful.'}, status=status.HTTP_400_BAD_REQUEST)

        if not hasattr(order, 'shipping') or order.shipping is None:
            return Response({'message': 'Shipping details not available.'}, status=status.HTTP_400_BAD_REQUEST)

        if order.shipping.delivery_status != 'Pending':  
            return Response({'message': 'Order is already shipped or delivered.'}, status=status.HTTP_400_BAD_REQUEST)

        order.shipping.delivery_status = 'Shipped'
        order.shipping.save()
        return Response({'message': 'Delivery shipped.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def deliver_delivery(self, request, *args, **kwargs):
        order = self.get_object()

        if not hasattr(order, 'shipping') or order.shipping is None:
            return Response({'message': 'Shipping details not available.'}, status=status.HTTP_400_BAD_REQUEST)

        if order.shipping.delivery_status != 'Shipped':  
            return Response({'message': 'Delivery not shipped yet.'}, status=status.HTTP_400_BAD_REQUEST)

        order.shipping.delivery_status = 'Delivered'
        order.shipping.save()
        return Response({'message': 'Delivery delivered.'}, status=status.HTTP_200_OK)


class UserShippingView(GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    serializer_class = ShippingSerializer
    queryset = Shipping.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Shipping.objects.filter(order__cart__user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        obj = super().get_object()
        if obj not in queryset:
            raise PermissionDenied("You do not have permission to view this shipping.")
        return obj


class AdminShippingView(GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    serializer_class = ShippingSerializer
    queryset = Shipping.objects.all()
    permission_classes = [permissions.IsAdminUser]








