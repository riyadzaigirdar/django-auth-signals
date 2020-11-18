from rest_framework import serializers
from blog import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "last_login",
            "is_superuser",
            "username",
            "email",
            "date_joined",
            ]

class UserRepresentation(serializers.RelatedField):
    def to_representation(self, value):
        return {
            "username" : value.username,
            "email" : value.email
            }

class BlogPostSerializer(serializers.ModelSerializer):
    # author = serializers.HyperlinkedRelatedField(read_only=True,view_name="blog-detail")
    # author = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='email'
    #  )
    author = UserRepresentation(read_only=True)
    class Meta:
        model = models.BlogPost
        fields = [
            'id',
            'title',
            'body',
            'image_png',
            'image',
            'video',
            'date_published',
            'date_updated',
            'slug',
            'author',
        ]
        read_only_fields = ['id', 'date_published', 'date_updated', 'slug']

class BlogPostSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BlogPost
        fields = [
            'id',
            'title',
            'body',
            'image_png',
            'image',
            'video',
            'author',
        ]
        read_only_fields=['id']