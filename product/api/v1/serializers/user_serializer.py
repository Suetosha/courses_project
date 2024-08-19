from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from users.models import Subscription, Balance

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""

    class Meta:
        model = User


class BalanceSerializer(serializers.ModelSerializer):
    """Сериализатор баланса пользователя."""
    class Meta:
        model = Balance
        fields = ('id', 'user', 'bonus')


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки."""

    # TODO

    class Meta:
        model = Subscription
        fields = (
            # TODO
        )
