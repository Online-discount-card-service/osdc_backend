from api.serializers import (CardEditSerializer, CardsListSerializer,
                             CardSerializer, GroupSerializer, ShopSerializer,
                             UserCustomCreateSerializer, UserReadSerializer)
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import exceptions

from core.models import Card, Group, Shop, UserCards


User = get_user_model()


class CardSerializerTest(TestCase):
    """Тестирование сериализатора CardSerializer."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.shop = Shop.objects.create(
            name='TestShop',
            color='pink',
        )
        cls.card = Card.objects.create(
            name='TestCard',
            shop=cls.shop,
            image='path/to/image.jpg',
            card_number='123456789',
            barcode_number='987654321',
            encoding_type='EAN-13',
            usage_counter=1,
        )
        cls.serializer = CardSerializer(instance=cls.card)

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
        self.assertEqual(set(self.serializer.data.keys()), expected_fields)

    def test_serializer_shop_representation(self):
        expected_representation = {
            'id': self.shop.id,
            'group': [],
            'name': 'TestShop',
            'logo': None,
            'color': 'pink',
            'validation': False,
        }
        self.assertEqual(
            self.serializer.data['shop'],
            expected_representation
        )


class GroupSerializerTest(TestCase):
    """Тестирование сериализатора Group."""

    def setUp(self):
        self.group = Group.objects.create(name='Test Group 1')
        self.serializer = GroupSerializer(instance=self.group)

    def test_serializer_data(self):
        expected_data = {
            'id': 1,
            'name': 'Test Group 1',
        }
        self.assertEqual(self.serializer.data, expected_data)


class ShopSerializerTest(TestCase):
    """Тестирование сериализатора Shop."""

    def setUp(self):
        self.shop = Shop.objects.create(
            name='Test Shop 1',
            color='green',
        )
        self.serializer = ShopSerializer(instance=self.shop)

    def test_serializer_data(self):
        expected_data = {
            'id': self.shop.id,
            'group': [],
            'name': 'Test Shop 1',
            'logo': None,
            'color': 'green',
            'validation': False,
        }
        self.assertEqual(self.serializer.data, expected_data)


class CardEditAndListSerializerTest(TestCase):
    """Тестирование сериализатора CardEdit и CardList."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            email='test@example.com',
            username='testuser',
            password='Qwe1346',
            phone_number='7248248742'
        )
        cls.shop = Shop.objects.create(
            name='TestShop',
            color='yellow',
        )
        cls.card = Card.objects.create(
            name='Test Card 1',
            shop=cls.shop,
            image='path/to/image.jpg',
            card_number='123456789',
            barcode_number='987654321',
        )
        cls.broken_card = Card.objects.create(
            name='Test Card 1',
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
        expected_data = {
            'card': {
                'id': self.card.id,
                'shop': self.list_serializer.data['card']['shop'],
                'name': 'Test Card 1',
                'pub_date': self.list_serializer.data['card']['pub_date'],
                'image': '/media/path/to/image.jpg',
                'card_number': '123456789',
                'barcode_number': '987654321',
                'encoding_type': 'ean-13',
                'usage_counter': 0,
            },
            'owner': True,
            'favourite': False,
        }
        self.assertEqual(self.list_serializer.data, expected_data)

    def test_edit_serializer_data(self):
        expected_data = {
            'id': self.card.id,
            'image': '/media/path/to/image.jpg',
            'shop': self.shop.id,
            'name': 'Test Card 1',
            'pub_date': self.edit_serializer.data['pub_date'],
            'card_number': '123456789',
            'barcode_number': '987654321',
            'encoding_type': 'ean-13',
        }
        self.assertEqual(self.edit_serializer.data, expected_data)

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
            'username': 'testUsERS',
            'phone_number': '9123456756',
            'password': 'testpassWORD',
        }

    def test_user_create_serializer(self):
        serializer = UserCustomCreateSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())

    def test_user_read_serializer(self):
        user = User.objects.create(**self.user_data)
        serializer = UserReadSerializer(instance=user)
        self.assertTrue(serializer.data)
