from django.shortcuts import get_object_or_404
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import permissions, serializers

from core.models import Card, UserCards


class IsCardsUser(permissions.BasePermission):
    """Разрешения: объект можно читать, редактировать может только автор."""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method == 'PATCH':
            user_card = get_object_or_404(UserCards, user=user, card=obj)
            return user_card.owner
        return UserCards.objects.filter(user=user, card=obj).exists


class IsShopCreatorOrReadOnly(permissions.IsAuthenticated):
    """Разрешения: магазины можно читать, редактировать может только автор."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'PATCH':
            user = request.user
            card = Card.objects.get(shop=obj)
            user_card = get_object_or_404(UserCards, user=user, card=card)
            return (
                user_card.owner
                and not obj.validation
            )
        return False


class IsUserEmailOwner(permissions.IsAuthenticated):
    """Разрешения: подтвердить можно только свою почту."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        uid = request.data.get('uid')
        if uid is None:
            raise serializers.ValidationError(
                {'uid': 'Обязательное поле.'})

        try:
            id_from_email = int(
                force_str(
                    urlsafe_base64_decode(uid)
                )
            )
        except (KeyError, TypeError, ValueError):
            raise serializers.ValidationError(
                {'uid': 'Неверный формат uid.'})

        return request.user.id == id_from_email
