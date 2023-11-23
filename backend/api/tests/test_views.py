from django.contrib.auth import get_user_model
from rest_framework import status

from core.models import Card

from .fixtures import APITests


User = get_user_model()


class CardAPITestCase(APITests):
    """Тестирование CardViewSet."""

    def test_filter_by_keyword(self):
        data = {'name': 'Несуществующая карт'}
        response = self.client.get(self.CARD_LIST_URL, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_cards(self):
        response = self.client.get(self.CARD_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_card(self):
        response = self.client.get(f'/api/v1/cards/{self.card.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_card(self):
        CARD_DATA = {
            'name': 'Test СarD',
            # 'shop': shop,
            'card_number': '234545564454',
            'barcode_number': '987635355355',
            'encoding_type': 'ean-13',
        }
        response = self.client.post(self.CARD_LIST_URL, CARD_DATA)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertTrue(
            Card.objects.filter(card_number='234545564454').exists()
        )

    def test_update_card(self):
        CARD_UPDATE_DATA = {
            'name': 'UPDATE СARD',
            # 'shop': cls.shop.id,
            'card_number': '190045564454',
            'barcode_number': '190035355355',
            'encoding_type': 'ean-8',
        }
        response = self.client.patch(
            f'/api/v1/cards/{self.card.id}/',
            CARD_UPDATE_DATA,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.card.refresh_from_db()
        self.assertEqual(self.card.card_number, '190045564454')

    def test_partial_update_card(self):
        CARD_PARTIAL_UPDATE_DATA = {
            'card_number': '111145564454',
        }
        response = self.client.patch(
            f'/api/v1/cards/{self.card.id}/',
            CARD_PARTIAL_UPDATE_DATA
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
        response = self.client.get(self.SHOP_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GroupViewSetTests(APITests):
    """Тестирование GroupViewSet."""

    def test_group_list(self):
        response = self.client.get(self.GROUP_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserViewSetTests(APITests):
    """Тестирование UserViewSet."""

    def test_me_get(self):
        response = self.client.get(self.USER_ME_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_me_patch(self):
        data = {'name': 'newusername'}
        response = self.client.patch(self.USER_ME_URL, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'newusername')
