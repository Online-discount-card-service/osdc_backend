from api.serializers import CardSerializer, GroupSerializer, ShopSerializer
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from core.models import Card, Group, Shop, UserCards


User = get_user_model()


class APITests(APITestCase):
    """Родительский класс с тестовыми данными и константами."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(name='Test Group')
        cls.group_serializer = GroupSerializer(instance=cls.group)
        cls.shop = Shop.objects.create(
            name='Test Shop',
            color='pink',
        )
        cls.shop_serializer = ShopSerializer(instance=cls.shop)
        cls.shop.group.set([cls.group])
        cls.card = Card.objects.create(
            name='Test Card',
            shop=cls.shop,
            image='path/to/image.jpg',
            card_number='123456789',
            barcode_number='987654321',
            encoding_type='ean-13',
            usage_counter=1,
        )
        cls.card_serializer = CardSerializer(instance=cls.card)
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
        cls.user = User.objects.create_user(
            email='user@example.com',
            name='TestUser',
            password='TestPass1',
        )
        user_card_data = {
            'user': cls.user,
            'card': cls.card,
            'owner': True,
        }
        cls.user_card = UserCards.objects.create(**user_card_data)
        cls.CARD_LIST = reverse('api:card-list')
        # cls.CARD_DETAIL = reverse(
        #     'api:card-detail',
        #     kwargs={'card-id': f'{cls.card.id}'}
        # )
        cls.SHOP_LIST = reverse('api:shop-list')
        cls.GROUP_LIST = reverse('api:group-list')
        cls.USER_ME = reverse('api:user-me')

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(
            user=self.user
        )
