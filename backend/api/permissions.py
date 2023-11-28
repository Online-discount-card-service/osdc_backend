from django.shortcuts import get_object_or_404
from rest_framework import permissions

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
        return (request.user.is_authenticated
                and UserCards.objects.filter(user=user, card=obj).exists)


class IsShopCreatorOrReadOnly(permissions.IsAuthenticated):
    """Разрешения: магазины можно читать, редактировать может только автор."""

    def has_object_permission(self, request, view, obj):
        if request.method == 'PATCH':
            user = request.user
            card = Card.objects.get(shop=obj)
            user_card = get_object_or_404(UserCards, user=user, card=card)
            return (
                user_card.owner
                and not obj.validation
            )
        return request.method in permissions.SAFE_METHODS
