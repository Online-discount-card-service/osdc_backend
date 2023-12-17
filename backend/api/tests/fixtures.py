import shutil
import tempfile

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
            content=b'\x47\x49\x46\x38\x39\x61\x02\x00\x01\x00\x80'
                    b'\x00\x00\x00\x00\x00\xFF\xFF\xFF\x21\xF9\x04'
                    b'\x00\x00\x00\x00\x00\x2C\x00\x00\x00\x00\x02'
                    b'\x00\x01\x00\x00\x02\x02\x0C\x0A\x00\x3B',
            content_type='image/gif',
        )
        cls.CARDS_USER_HAVE = 17
        # NOTE: CARDS_USER_OWN должно быть
        # меньше хотя бы на 1 чем CARDS_USER_HAVE
        cls.CARDS_USER_OWN = 10
        cls.CARDS_USER_FAV = 5
        cls.CARDS_USER_NOT_HAVE = 3
        cls.SHOPS = 9
        cls.SHOPS_VERIFY = 5
        cls.GROUPS = 5
        cls.USERS = 3
        cls.EMAIL_NOT_OF_A_USER = 'share-invitation-test@example.com'

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
            )
        cls.card = Card.objects.order_by().first()

        for user_num in range(cls.USERS):
            cls.user = User.objects.create_user(
                email=f'user{user_num}@example.com',
                password=f'TestPass{user_num}',
                phone_number=f'+7999999999{user_num}',
            )
        cls.user = User.objects.order_by().first()
        cls.user.is_active = True
        cls.another_user = User.objects.order_by()[1]
        cls.unactivated_user = User.objects.order_by()[2]
        cls.unactivated_user.is_active = False

        for card_num in range(cls.CARDS_USER_HAVE):
            UserCards.objects.create(
                user=cls.user,
                card=Card.objects.get(card_number=f'{card_num}'),
                owner=(card_num < cls.CARDS_USER_OWN),
                favourite=(card_num < cls.CARDS_USER_FAV),
            )
        cls.card_user_not_own = Card.objects.get(
            card_number=f'{cls.CARDS_USER_OWN}'
        )
        cls.card_user_not_fav = Card.objects.get(
            card_number=f'{cls.CARDS_USER_FAV}'
        )
        card_user_own = UserCards.objects.filter(
            user=cls.user,
            owner=True
        ).order_by().first()
        cls.card_user_own = card_user_own.card

        cls.CARDS_URL = reverse('api:card-list')
        cls.CARD_DETAIL_URL = reverse(
            'api:card-detail',
            kwargs={'pk': f'{cls.card.id}'}
        )
        cls.GROUP_LIST_URL = reverse('api:group-list')

    def setUp(self):
        self.guest_client = APIClient()
        self.auth_client = APIClient()
        self.inactive_auth_client = APIClient()
        self.auth_client.force_authenticate(user=self.user)
        self.inactive_auth_client.force_authenticate(
            user=self.unactivated_user
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)


class APIShopEditTests(APITests):
    """Родительский класс с тестовыми данными и константами."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        for group_num in range(cls.GROUPS):
            Group.objects.create(name=f'Test Group #{group_num}')
        cls.group = Group.objects.order_by().first()

        cls.shop_unvalidated = Shop.objects.create(
            name='Test Unvalidated Shop',
            validation=False,
        )
        cls.shop_unvalidated_from_friends_card = Shop.objects.create(
            name='Test Unvalidated Shop from friends card',
            validation=False,
        )
        cls.shop_validated = Shop.objects.create(
            name='Validated Shop',
            validation=True
        )

        cls.card_unvalidated_shop = Card.objects.create(
            name='Test Card With Unvalidated Shop',
            shop=cls.shop_unvalidated,
            card_number='12345678',
        )
        cls.card_unvalidated_from_friend = Card.objects.create(
            name='Test Card Shared By Friend',
            shop=cls.shop_unvalidated_from_friends_card
        )
        cls.card_validated_shop = Card.objects.create(
            name='Test Card With Validated Shop',
            shop=cls.shop_validated
        )

        UserCards.objects.create(
            user=cls.user,
            card=cls.card_unvalidated_shop,
            owner=True,
            favourite=False,
        )
        UserCards.objects.create(
            user=cls.user,
            card=cls.card_unvalidated_from_friend,
            owner=False,
            favourite=False,
        )
        UserCards.objects.create(
            user=cls.user,
            card=cls.card_validated_shop,
            owner=True,
            favourite=False,
        )
