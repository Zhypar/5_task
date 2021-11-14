from rest_framework import generics

from market.models import Comments
from market.serializers import (
    CreateCommentSerializer,
    CreateRelpliesSerializer,
    UpdateCommentSerializer,
    GetCommentSerializer,
)
from rest_framework import permissions


class CreateCommentView(generics.CreateAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CreateCommentSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class CreateRepliesView(generics.CreateAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CreateRelpliesSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class DeleteCommentByIdView(generics.DestroyAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    queryset = Comments.objects.all()


class UpdateCommentByIdView(generics.UpdateAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    queryset = Comments.objects.all()
    serializer_class = UpdateCommentSerializer

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class GetCommentView(generics.ListAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    queryset = Comments.objects.filter(replies=None)
    serializer_class = GetCommentSerializer


class FindCommentByIdView(generics.RetrieveAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    queryset = Comments.objects.all()
    serializer_class = GetCommentSerializer
