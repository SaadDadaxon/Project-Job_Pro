from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Jobs, Like, ApplyJob
from account.serializer import MyAccountSerializer


class JobGETSerializer(serializers.ModelSerializer):
    # author = MyAccountSerializer(read_only=True)

    class Meta:
        model = Jobs
        fields = ('id', 'author', 'title', 'company', 'location', 'category', 'type', 'price', 'tags', 'created_date')


class JobPOSTSerializer(serializers.ModelSerializer):

    class Meta:
        model = Jobs
        fields = ('id', 'author', 'title', 'company', 'location', 'category', 'type', 'price', 'tags', 'created_date')
        extra_kwargs = {
            'author': {'required': False}
        }

    def validate(self, attrs):
        request = self.context['request']
        author = request.user
        if author.role == 1:
            raise ValidationError('Siz Xodim izlab bilmaysiz')
        if author.role == 2:
            raise ValidationError('Siz Admin siz ishingizni qiling')
        return attrs

    def create(self, validated_data):
        request = self.context['request']
        author = request.user
        instance = super().create(validated_data)
        instance.author = author
        instance.save()
        return instance


class LikeGETSerializer(serializers.ModelSerializer):
    author = MyAccountSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'author', 'jobs')


class LikePOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'author', 'jobs')

    def create(self, validated_data):
        request = self.context['request']
        author = request.user
        instance = super().create(**validated_data)
        instance.author = author
        return instance


class ApplyJobGETSerializer(serializers.ModelSerializer):
    author = MyAccountSerializer(read_only=True)
    jobs = JobGETSerializer(read_only=True)

    class Meta:
        model = ApplyJob
        fields = ('id', 'author', 'jobs', 'rezume')


class ApplyJobPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyJob
        fields = ('id', 'author', 'jobs', 'rezume')
        extra_kwargs = {
            'author': {'read_only': True},
        }

    def validate(self, attrs):
        request = self.context['request']
        author = request.user
        if author.role == 0:
            raise ValidationError('You are a HR')
        if author.role == 2:
            raise ValidationError('You are a Admin')
        return attrs

    def create(self, validated_data):
        request = self.context['request']
        author = request.user
        instance = super().create(validated_data)
        instance.author = author
        return instance



