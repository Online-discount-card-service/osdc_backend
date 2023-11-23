import shutil
import tempfile

from api.serializers import CardSerializer, GroupSerializer, ShopSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from core.models import Card, Group, Shop, UserCards


TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
User = get_user_model()


class APITests(APITestCase):
    """Родительский класс с тестовыми данными и константами."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.UPLOADED_GIF = SimpleUploadedFile(
            name='small.gif',
            content=(
                b'\x47\x49\x46\x38\x39\x61\x02\x00'
                b'\x01\x00\x80\x00\x00\x00\x00\x00'
                b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
                b'\x00\x00\x00\x2C\x00\x00\x00\x00'
                b'\x02\x00\x01\x00\x00\x02\x02\x0C'
                b'\x0A\x00\x3B'
            ),
            content_type='image/gif',
        )
        cls.CARDS_USER_HAVE = 17
        cls.CARDS_USER_OWN = 10
        cls.CARDS_USER_FAV = 5
        cls.CARDS_USER_NOT_HAVE = 3
        cls.SHOPS = 9
        cls.SHOPS_VERIFY = 5
        cls.GROUPS = 5

        for group_num in range(cls.GROUPS):
            Group.objects.create(name=f'Test Group #{group_num}')
        cls.group = Group.objects.order_by().first()

        for shop_num in range(cls.SHOPS):
            shop = Shop.objects.create(
                name=f'Test Shop #{shop_num}',
                color='#AABBCC',
                logo=cls.UPLOADED_GIF,
                validation=(shop_num < cls.SHOPS_VERIFY),
            )
            shop.group.set([cls.group])
        cls.shop = Shop.objects.order_by().first()

        for card_num in range(cls.CARDS_USER_HAVE + cls.CARDS_USER_NOT_HAVE):
            Card.objects.create(
                name=f'Test Card #{card_num}',
                shop=cls.shop,
                image=cls.UPLOADED_GIF,
                card_number=f'{card_num}',
                barcode_number=f'{card_num}',
                encoding_type='ean-13',
                usage_counter=1,
            )
        cls.card = Card.objects.order_by().first()

        cls.user = User.objects.create_user(email='user@example.com')

        for card_num in range(cls.CARDS_USER_HAVE):
            UserCards.objects.create(
                user=cls.user,
                card=Card.objects.get(card_number=f'{card_num}'),
                owner=(card_num < cls.CARDS_USER_OWN),
                favorite=(card_num < cls.CARDS_USER_FAV),
            )

        cls.group_serializer = GroupSerializer(instance=cls.group)
        cls.shop_serializer = ShopSerializer(instance=cls.shop)
        cls.card_serializer = CardSerializer(instance=cls.card)

        cls.CARD_LIST_URL = reverse('api:card-list')
        cls.CARD_DETAIL_URL = reverse(
            'api:card-detail',
            kwargs={'pk': f'{cls.card.id}'}
        )
        cls.SHOP_LIST_URL = reverse('api:shop-list')
        cls.GROUP_LIST_URL = reverse('api:group-list')
        cls.USER_ME_URL = reverse('api:user-me')

    def setUp(self):
        self.guest_client = APIClient()
        self.client = APIClient()
        self.client.force_login(self.self.user)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
