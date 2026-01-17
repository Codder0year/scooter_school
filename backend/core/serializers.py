from rest_framework import serializers
from .models import News


class NewsSerializer(serializers.ModelSerializer):
    # image и video по умолчанию дают URL (use_url=True)
    image = serializers.ImageField(read_only=True)
    video = serializers.FileField(read_only=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'date_posted', 'image', 'video']
        read_only_fields = ['id', 'date_posted']
