from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Blog, Comment
from .permission import IsOwnerOrReadOnly
from rest_framework.response import Response
from .serializer import BlogPOSTSerializer, BlogGETSerializer, CommentSerializer


class BlogListCreate(generics.ListCreateAPIView):
    # http://127.0.0.1:8000/blog/api/list-create/
    queryset = Blog.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BlogGETSerializer
        return BlogPOSTSerializer


class BlogRUD(generics.RetrieveUpdateDestroyAPIView):
    # http://127.0.0.1:8000/blog/api/rud/<int:pk>/
    queryset = Blog.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BlogGETSerializer
        return BlogPOSTSerializer


class CommentListCreate(generics.ListCreateAPIView):
    queryset = Comment.objects.filter(parent_comment__isnull=True)
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['blog_id'] = self.kwargs.get('blog_id')
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()
        blog_id = self.kwargs.get('blog_id')
        qs = qs.filter(blog_id=blog_id)
        return qs


