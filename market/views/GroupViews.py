from django.contrib.auth.models import Group
from rest_framework import generics

from market.serializers import AllGroupSerializer


class CreateGroupView(generics.CreateAPIView):

    serializer_class = AllGroupSerializer


class DeleteGroupByIdView(generics.DestroyAPIView):

    queryset = Group.objects.all()
    serializer_class = AllGroupSerializer


class UpdateGroupByIdView(generics.UpdateAPIView):

    queryset = Group.objects.all()
    serializer_class = AllGroupSerializer


class GetGroupView(generics.ListAPIView):

    queryset = Group.objects.all()
    serializer_class = AllGroupSerializer


class FindGroupByIdView(generics.RetrieveAPIView):

    queryset = Group.objects.all()
    serializer_class = AllGroupSerializer
