from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response

from market.models import Product
from market.serializers import (
    CreateProductSerializer,
    UpdateProductSerializer,
    GetProductSerializer,
)
from rest_framework import permissions


class CreateProductView(generics.CreateAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CreateProductSerializer


class DeleteProductByIdView(generics.DestroyAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    queryset = Product.objects.all()


class DeleteAllProductView(generics.DestroyAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        try:
            return Product.objects.all()
        except Product.DoesNotExist:
            raise Http404

    def delete(self, request, format=None, **kwargs):
        """Метод удаления всех товаров"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateProductByIdView(generics.UpdateAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = UpdateProductSerializer


class GetProductView(generics.ListAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = GetProductSerializer


class FindProductByIdView(generics.RetrieveAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = GetProductSerializer
