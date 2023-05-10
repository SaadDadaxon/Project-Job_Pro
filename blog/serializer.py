from rest_framework import serializers
from .models import Blog, Comment
from account.serializer import MyAccountSerializer


class BlogGETSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = ('id', 'author', 'title', 'category', 'image', 'text', 'created_date')


class BlogPOSTSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = ('id', 'author', 'title', 'category', 'image', 'text', 'created_date')
        extra_kwargs = {
            'category': {'required': False},
            'author': {'read_only': False},
            'blog': {'read_only': True},
            'image': {'required': False},
        }

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        instance = super().create(validated_data)
        instance.author = author
        instance.save()
        return instance


class MiniCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'author', 'blog', 'body', 'top_level_comment_id', 'created_date')


class CommentSerializer(serializers.ModelSerializer):
    author = MyAccountSerializer(read_only=True)
    children = serializers.SerializerMethodField(read_only=True)

    def get_children(self, obj):
        children = Comment.objects.filter(parent_comment_id=obj.id)
        serializer = MiniCommentSerializer(children, many=True)
        return serializer.data

    class Meta:
        model = Comment
        fields = ('id', 'author', 'blog', 'body', 'parent_comment', 'children', 'top_level_comment_id', 'created_date')
        extra_kwargs = {
            'author': {'read_only': True},
            'blog': {'read_only': True},
            'top_level_comment_id': {'read_only': True},
        }

    def create(self, validated_data):
        request = self.context['request']
        blog_id = self.context['blog_id']
        author_id = request.user.id
        instance = Comment.objects.create(author_id=author_id, blog_id=blog_id, **validated_data)
        return instance

