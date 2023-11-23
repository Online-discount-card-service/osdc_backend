from api.serializers import (CardEditSerializer, CardsListSerializer,
                             UserCustomCreateSerializer, UserReadSerializer)
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import exceptions

from core.models import Card, Group, Shop, UserCards

from .fixtures import APITests


User = get_user_model()


class CardSerializerTest(APITests):
    """Тестирование сериализатора CardSerializer."""

    def test_serializer_fields(self):
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
        self.assertEqual(
            set(self.card_serializer.data.keys()),
            expected_fields,
        )

    def test_serializer_shop_representation(self):
        shop = self.card_serializer.data['shop']
        expected_representation = {
            'id': self.shop.id,
            'group': shop['group'],
            'name': 'Test Shop',
            'logo': None,
            'color': 'pink',
            'validation': False,
        }
        self.assertEqual(shop, expected_representation)


class GroupSerializerTest(APITests):
    """Тестирование сериализатора Group."""

    def test_serializer_data(self):
        expected_data = {
            'id': 1,
            'name': 'Test Group',
        }
        self.assertEqual(self.group_serializer.data, expected_data)


class ShopSerializerTest(APITests):
    """Тестирование сериализатора Shop."""

    def test_serializer_data(self):
        shop = self.shop_serializer.data
        expected_data = {
            'id': self.shop.id,
            'group': shop['group'],
            'name': 'Test Shop',
            'logo': None,
            'color': 'pink',
            'validation': False,
        }
        self.assertEqual(shop, expected_data)


class CardEditAndListSerializerTest(APITests):
    """Тестирование сериализатора CardEdit и CardList."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            email='test@example.com',
            name='testuser',
            password='Qwe1346',
            phone_number='7248248742',
        )
        cls.broken_card = Card.objects.create(
            name='Broken Card',
            shop=cls.shop,
            image='path/to/image.jpg',
            card_number='',
            barcode_number='',
        )
        cls.user_card = UserCards.objects.create(
            user=cls.user,
            card=cls.card,
        )
        cls.list_serializer = CardsListSerializer(instance=cls.user_card)
        cls.edit_serializer = CardEditSerializer(instance=cls.card)
        cls.broken_serializer = CardEditSerializer(instance=cls.broken_card)

    def test_list_serializer_data(self):
        list_data = self.list_serializer.data
        expected_data = {
            'card': {
                'id': self.card.id,
                'shop': list_data['card']['shop'],
                'image': '/media/path/to/image.jpg',
                'name': 'Test Card',
                'pub_date': list_data['card']['pub_date'],
                'card_number': '123456789',
                'barcode_number': '987654321',
                'encoding_type': 'ean-13',
                'usage_counter': 1,
            },
            'owner': True,
            'favourite': False,
        }
        self.assertEqual(list_data, expected_data)

    def test_edit_serializer_data(self):
        edit_data = self.edit_serializer.data
        expected_data = {
            'id': self.card.id,
            'shop': edit_data['shop'],
            'image': '/media/path/to/image.jpg',
            'name': 'Test Card',
            'pub_date': edit_data['pub_date'],
            'card_number': '123456789',
            'barcode_number': '987654321',
            'encoding_type': 'ean-13',
            'usage_counter': 1,
        }
        self.assertEqual(edit_data, expected_data)

    def test_validation_error(self):
        error_message = 'Необходимо указать номер карты и/или штрих-кода'

        with self.assertRaises(exceptions.ValidationError) as context:
            self.broken_serializer.validate(self.broken_serializer.data)

        self.assertEqual(
            str(context.exception.detail[0]),
            error_message
        )


class UserSerializersTest(TestCase):
    """Тестирование сериализаторов User'а для создания и чтения."""

    def setUp(self):
        self.user_data = {
            'email': 'test_email@example.com',
            'name': 'testUsERS',
            'phone_number': '9123456756',
            'password': 'testpassWORD12',
        }

    def test_user_create_serializer(self):
        serializer = UserCustomCreateSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())

    def test_user_read_serializer(self):
        user = User.objects.create(**self.user_data)
        serializer = UserReadSerializer(instance=user)
        self.assertTrue(serializer.data)
