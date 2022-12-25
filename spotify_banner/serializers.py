from rest_framework import serializers


class ReadOnlySerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        raise ValueError('Cannot update a read-only serializer')

    def create(self, validated_data):
        raise ValueError('Cannot create a read-only serializer')


class ArtistSerializer(ReadOnlySerializer):
    name = serializers.CharField(max_length=255)
    href = serializers.URLField(source='external_urls.spotify')


class ImageSerializer(ReadOnlySerializer):
    url = serializers.URLField()
    width = serializers.IntegerField()
    height = serializers.IntegerField()


class TrackSerializer(ReadOnlySerializer):
    artists = ArtistSerializer(many=True)
    duration_ms = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    href = serializers.URLField(source='external_urls.spotify')
    preview_url = serializers.URLField()
    explicit = serializers.BooleanField()
    images = ImageSerializer(many=True, source='album.images')


class CurrentTrackSerializer(ReadOnlySerializer):
    track = TrackSerializer(source='item')
    progress_ms = serializers.IntegerField()
    is_playing = serializers.BooleanField()
