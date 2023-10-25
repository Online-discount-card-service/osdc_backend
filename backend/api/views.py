from djoser.views import UserViewSet
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)


class UserViewSet(UserViewSet):
    """Набор представлений для просмотра и редактирования
    пользовательских экземпляров."""
    permission_classes = (IsAuthenticatedOrReadOnly,)
