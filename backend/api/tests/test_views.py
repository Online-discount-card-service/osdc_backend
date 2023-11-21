from api.serializers import CardSerializer
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Card, Group, Shop, UserCards


User = get_user_model()


class CardAPITestCase(TestCase):
    """Тестирование CardViewSet."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(name='Test group')
        cls.shop = Shop.objects.create(name='Test shop')
        cls.shop.group.set([cls.group])
        cls.card = Card.objects.create(
            name='Test Сard',
            shop=cls.shop,
            card_number='23456789',
            barcode_number='98765432',
            encoding_type='ean-13',
        )
        cls.DATA_CARD = {
            'name': 'Test СarD',
            'shop': cls.shop.id,
            'card_number': '234545564454',
            'barcode_number': '987635355355',
            'encoding_type': 'ean-13',
        }
        cls.UPDATE_DATA_CARD = {
            'name': 'UPDATE СARD',
            'shop': cls.shop.id,
            'card_number': '190045564454',
            'barcode_number': '190035355355',
            'encoding_type': 'ean-8',
        }
        cls.PARTIAL_UPDATE_DATA_CARD = {
            'card_number': '111145564454',
        }
        cls.serializer = CardSerializer(instance=cls.card)
        cls.user = User.objects.create_user(
            username='TestUser',
            password='TestPass',
        )
        user_card_data = {
            'user': cls.user,
            'card': cls.card,
            'owner': True,
        }
        cls.user_card = UserCards.objects.create(**user_card_data)

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(
            user=self.user
        )

    def test_card_fields(self):
        expected_fields = {
            'id',
            'name',
            'shop',
            'pub_date',
            'image',
            'card_number',
            'barcode_number',
            'encoding_type',
            'usage_counter',
        }
        serializer_data = CardSerializer(instance=self.card).data
        self.assertEqual(set(serializer_data.keys()), expected_fields)

    def test_filter_by_keyword(self):
        url = reverse('api:card-list')
        data = {'name': 'Несуществующая карт'}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_cards(self):
        response = self.client.get('/api/v1/cards/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_card(self):
        response = self.client.get(f'/api/v1/cards/{self.card.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_card(self):
        response = self.client.post('/api/v1/cards/', self.DATA_CARD)
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


class ShopViewSetTests(TestCase):
    """Тестирование ShopViewSet."""

    def setUp(self):
        self.client = APIClient()

    def test_shop_list(self):
        response = self.client.get('/api/v1/shops/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GroupViewSetTests(TestCase):
    """Тестирование GroupViewSet."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.force_authenticate(
            user=self.user
        )

    def test_group_list(self):
        response = self.client.get('/api/v1/groups/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserViewSetTests(TestCase):
    """Тестирование UserViewSet."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        self.client.force_authenticate(user=self.user)

    def test_me_get(self):
        response = self.client.get('/api/v1/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_me_patch(self):
        data = {'username': 'newusername'}
        response = self.client.patch('/api/v1/users/me/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'newusername')
