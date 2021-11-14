from rest_framework import generics

from market.models import Category
from market.serializers import (
    CreateCategorySerializer,
    UpdateCategorySerializer,
    GetCategorySerializer,
)


class CreateCategoryView(generics.CreateAPIView):

    serializer_class = CreateCategorySerializer


class DeleteCategoryByIdView(generics.DestroyAPIView):

    queryset = Category.objects.all()


class UpdateCategoryByIdView(generics.UpdateAPIView):

    queryset = Category.objects.all()
    serializer_class = UpdateCategorySerializer


class GetCategoryView(generics.ListAPIView):

    queryset = Category.objects.all()
    serializer_class = GetCategorySerializer


class FindCategoryByIdView(generics.RetrieveAPIView):

    queryset = Category.objects.all()
    serializer_class = GetCategorySerializer
