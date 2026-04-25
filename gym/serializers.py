from rest_framework import serializers

from .models import Class, Gym, Plans, Trainer


def _absolute_image_url(request, fieldfile):
    if not fieldfile:
        return None
    try:
        url = fieldfile.url
    except ValueError:
        return None
    if request:
        return request.build_absolute_uri(url)
    return url


class GymSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Gym
        fields = [
            'id',
            'owner_user_id',
            'name',
            'location',
            'featured',
            'image_url',
            'description',
            'address',
            'phone_number',
            'email',
            'created_at',
            'updated_at',
        ]

    def get_image_url(self, obj):
        return _absolute_image_url(self.context.get('request'), obj.image_url)


class ClassSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = [
            'id',
            'gym_id',
            'name',
            'duration',
            'number_of_classes',
            'price',
            'description',
            'image_url',
            'sort_order',
            'created_at',
            'updated_at',
        ]

    def get_image_url(self, obj):
        return _absolute_image_url(self.context.get('request'), obj.image_url)


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plans
        fields = [
            'id',
            'gym_id',
            'name',
            'duration',
            'price',
            'description',
            'features',
            'sort_order',
            'created_at',
            'updated_at',
            'classes',
        ]


class TrainerSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Trainer
        fields = [
            'id',
            'gym_id',
            'name',
            'experience',
            'image_url',
            'bio',
            'sort_order',
            'created_at',
            'updated_at',
        ]

    def get_image_url(self, obj):
        return _absolute_image_url(self.context.get('request'), obj.image_url)
