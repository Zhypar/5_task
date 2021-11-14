from rest_framework import generics

from market.models import CartItems
from market.serializers import (
    CreateCartItemsSerializer,
    UpdateCartItemsSerializer,
    GetCartItemsSerializer,
)
from rest_framework import permissions


class CreateCartItemsView(generics.CreateAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CreateCartItemsSerializer

    def perform_create(self, serializer):
        serializer.save(customer_id=self.request.user)


class DeleteCartItemsByIdView(generics.DestroyAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    queryset = CartItems.objects.all()


class UpdateCartItemsByIdView(generics.UpdateAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    queryset = CartItems.objects.all()
    serializer_class = UpdateCartItemsSerializer

    def perform_update(self, serializer):
        serializer.save(customer_id=self.request.user)


class GetCartItemsView(generics.ListAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    queryset = CartItems.objects.all()
    serializer_class = GetCartItemsSerializer


class FindCartItemsByIdView(generics.RetrieveAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    queryset = CartItems.objects.all()
    serializer_class = GetCartItemsSerializer
