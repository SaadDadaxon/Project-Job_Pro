from django.shortcuts import render
from rest_framework import generics, permissions, serializers
from rest_framework.response import Response

from .models import Jobs, Like, ApplyJob
from .serializer import JobGETSerializer, JobPOSTSerializer, LikeGETSerializer, LikePOSTSerializer, \
    ApplyJobPOSTSerializer, ApplyJobGETSerializer


class JobsListCreate(generics.ListCreateAPIView):
    queryset = Jobs.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return JobPOSTSerializer
        return JobGETSerializer


class LikeListCreate(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LikePOSTSerializer
        return LikeGETSerializer

    def create(self, request, *args, **kwargs):
        author_id = request.user.id
        jobs_id = self.kwargs.get('jobs_id')
        like = Like.objects.filter(author_id=author_id, jobs_id=jobs_id)
        if like:
            like.delete()
            return Response({'message': "Like Deleted Successfully!"})
        like = Like.objects.create(author_id=author_id, jobs_id=jobs_id)
        serializer = LikePOSTSerializer(like)
        return Response({'message': 'Like create Successfully!'}, serializer.data)


class ApplyCreate(generics.CreateAPIView):
    queryset = ApplyJob.objects.all()
    serializer_class = ApplyJobPOSTSerializer
    permission_classes = [permissions.IsAuthenticated]


class ApplyJobList(generics.ListAPIView):
    queryset = ApplyJob.objects.all()
    serializer_class = ApplyJobGETSerializer
    permission_classes = [permissions.IsAdminUser]


class ApplyList(generics.ListAPIView):
    queryset = ApplyJob.objects.all()
    serializer_class = ApplyJobGETSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        jobs_id = self.kwargs.get('jobs_id')
        author = self.request.user
        if qs:
            qs = qs.filter(jobs_id=jobs_id, author=author)
            if author.role == 1:
                raise serializers.ValidationError('You are not HR')
        return qs




