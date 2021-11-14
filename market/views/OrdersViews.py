from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response

from market.statuses import PURCHASED
from market.models import CartItems, Orders
from market.serializers import CreateOrderSerializer, GetOrderSerializer
from rest_framework import permissions


class CreateOrderView(generics.CreateAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CreateOrderSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            for order_items, product in zip(
                request.data["order_items"], CartItems.objects.all()
            ):
                order_items["prod_id"] = product.product_id.id
                order_items["title"] = product.product_id.title
                order_items["description"] = product.product_id.description
                order_items["amount"] = product.amount
                if order_items["price"].__eq__(int()):
                    order_items["price"] = product.product_id.price
                    self.perform_create(serializer, product)
                else:
                    self.perform_create(serializer, product)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer, product=None):
        serializer.save(client_id=self.request.user, status=PURCHASED)
        product.delete()


class DeleteOrderByIdView(generics.DestroyAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    queryset = Orders.objects.all()


class DeleteAllOrdersView(generics.DestroyAPIView):
    def get_object(self):
        try:
            return Orders.objects.all()
        except Orders.DoesNotExist:
            raise Http404

    def delete(self, request, format=None, **kwargs):

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetOrdersView(generics.ListAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    queryset = Orders.objects.all()
    serializer_class = GetOrderSerializer


class FindOrderByIdView(generics.RetrieveAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    queryset = Orders.objects.all()
    serializer_class = GetOrderSerializer
