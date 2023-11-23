from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from core.models import Card, Group, Shop, UserCards

from .fixtures import APITests


User = get_user_model()


class CardAPITestCase(APITests):
    """Тестирование CardViewSet."""

    def test_filter_by_keyword(self):
        data = {'name': 'Несуществующая карт'}
        response = self.client.get(self.CARD_LIST, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_cards(self):
        response = self.client.get(self.CARD_LIST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_card(self):
        response = self.client.get(reverse('api:card-detail', self.card.id))  # ???????
        # response = self.client.get(f'/api/v1/cards/{self.card.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_card(self):
        response = self.client.post(self.CARD_LIST, self.DATA_CARD)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertTrue(
            Card.objects.filter(card_number='234545564454').exists()
        )

    def test_update_card(self):
        response = self.client.patch(
            f'/api/v1/cards/{self.card.id}/',
            self.UPDATE_DATA_CARD,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.card.refresh_from_db()
        self.assertEqual(self.card.card_number, '190045564454')

    def test_partial_update_card(self):
        response = self.client.patch(
            f'/api/v1/cards/{self.card.id}/',
            self.PARTIAL_UPDATE_DATA_CARD
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.card.refresh_from_db()
        self.assertEqual(self.card.card_number, '111145564454')

    def test_destroy_card(self):
        response = self.client.delete(f'/api/v1/cards/{self.card.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Card.objects.filter(id=self.card.id).exists())


class ShopViewSetTests(APITests):
    """Тестирование ShopViewSet."""

    def test_shop_list(self):
        response = self.client.get(self.SHOP_LIST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GroupViewSetTests(APITests):
    """Тестирование GroupViewSet."""

    def test_group_list(self):
        response = self.client.get(self.GROUP_LIST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserViewSetTests(APITests):
    """Тестирование UserViewSet."""

    def test_me_get(self):
        response = self.client.get(self.USER_ME)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_me_patch(self):
        data = {'name': 'newusername'}
        response = self.client.patch(self.USER_ME, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'newusername')
