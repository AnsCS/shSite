from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    # email = serializers.EmailField()
    body = serializers.CharField()
    created_at = serializers.DateTimeField()
    post_slug = serializers.CharField(source='post.slug')


    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        # instance.email = validated_data.get('email', instance.email)
        instance.post_slug = validated_data.get('post_slug', instance.post_slug)
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance
