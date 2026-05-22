from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import Gym

User = get_user_model()


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Accept email + password instead of username."""

    username_field = 'email'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'] = serializers.EmailField()
        self.fields['password'] = serializers.CharField(write_only=True)
        if 'username' in self.fields:
            del self.fields['username']

    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()
        password = attrs.get('password', '')

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {'detail': 'Invalid email or password.'}
            ) from None

        if not user.check_password(password):
            raise serializers.ValidationError(
                {'detail': 'Invalid email or password.'}
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {'detail': 'This account is disabled.'}
            )

        refresh = self.get_token(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        gym = Gym.objects.filter(owner_user_id=user).first()

        if user.is_superuser or user.is_staff:
            role = 'admin'
        else:
            role = 'gym_owner'

        name = user.get_full_name().strip() or user.first_name or user.username

        return Response(
            {
                'id': user.pk,
                'email': user.email,
                'name': name,
                'role': role,
                'gym_id': gym.pk if gym else None,
            }
        )


class TokenRefreshPublicView(TokenRefreshView):
    """Refresh access token using a valid refresh token."""

    permission_classes = []
