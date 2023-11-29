from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse

from core.models import Card, UserCards

from .fixtures import APIShopEditTests, APITests


User = get_user_model()


class EndpointsTestCase(APITests):
    """Тестирование ручек."""

    def test_user_list_accessibility_for_guest(self):
        """Проверка недоступности ручки user-list без авторизации."""

        url = reverse('api:user-list')
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_list_accessibility_for_user(self):
        """Проверка выдачи user-list только одного пользователя."""

        url = reverse('api:user-list')
        response = self.auth_client.get(url)
        self.assertEqual(len(response.data), 1)

    def test_user_me_accessibility_for_user(self):
        """Проверка доступности ручки users/me."""

        url = reverse('api:user-me')
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_accessibility(self):
        """Проверка доступности ручки логина."""

        response = self.client.post(
            '/api/v1/auth/token/login/',
            {'email': self.user.email,
             'password': 'TestPass0'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_functionality(self):
        """Проверка функционирования ручки логина."""

        response = self.client.post(
            '/api/v1/auth/token/login/',
            {'email': self.user.email,
             'password': 'TestPass0'}
        )
        self.assertIn('auth_token', response.data)
        user_token = Token.objects.get(user=self.user)
        self.assertEqual(response.data['auth_token'], user_token.key)

    def test_cards_list_accessibility_for_guest(self):
        """Проверка недоступности ручки card-list без авторизации."""

        response = self.guest_client.get(self.CARDS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cards_list_count(self):
        """Проверка доступности и количества карт в card-list."""

        response = self.auth_client.get(self.CARDS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.CARDS_USER_HAVE)

    def test_cards_list_fields(self):
        """Проверка полей в card-list."""

        response = self.auth_client.get(self.CARDS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_fields = [
            'card', 'owner', 'favourite', 'usage_counter',
        ]
        expected_card_fields = [
            'id', 'shop', 'image', 'name', 'pub_date', 'card_number',
            'barcode_number', 'encoding_type',
        ]
        expected_shop_fields = [
            'id', 'group', 'logo', 'name', 'color', 'validation',
        ]
        expected_group_fields = [
            'id', 'name',
        ]
        for card_data in response.data:
            self.assertTrue(
                all(field in card_data
                    for field in expected_fields))
            self.assertTrue(
                all(field in card_data['card']
                    for field in expected_card_fields))
            shop_data = card_data['card']['shop']
            self.assertTrue(
                all(field in shop_data
                    for field in expected_shop_fields))
            group_data = shop_data['group'][0]
            self.assertTrue(
                all(field in group_data
                    for field in expected_group_fields))

    def test_card_accessibility_for_user(self):
        """Проверка доступности ручки card-detail."""

        url = reverse('api:card-detail', kwargs={'pk': self.card.pk})
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_card_accessibility_for_guest(self):
        """Проверка недоступности ручки card-detail без авторизации."""

        response = self.guest_client.get(self.CARD_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cards_card_detail_fields(self):
        """Проверка полей в card detail."""

        response = self.auth_client.get(self.CARD_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_card_fields = [
            'id', 'shop', 'image', 'name', 'pub_date', 'card_number',
            'barcode_number', 'encoding_type',
        ]
        expected_shop_fields = [
            'id', 'group', 'logo', 'name', 'color', 'validation'
        ]
        expected_group_fields = [
            'id', 'name'
        ]
        self.assertTrue(
            all(field in response.data for field in expected_card_fields))
        shop_data = response.data['shop']
        self.assertTrue(
            all(field in shop_data for field in expected_shop_fields))
        group_data = response.data['shop']['group'][0]
        self.assertTrue(
            all(field in group_data for field in expected_group_fields))

    def assert_user_has_new_card(self, new_card_pk):
        """Метод для проверки, что у пользователя появилась новая карта."""

        self.assertTrue(
            UserCards.objects.filter(
                user=self.user, card__pk=new_card_pk).exists(),
            'У пользователя не появилась новая карта.'
        )
        user_card = UserCards.objects.get(user=self.user, card__pk=new_card_pk)
        self.assertTrue(user_card.owner,
                        'Пользователь не является владельцем новой карты.')

    def test_card_create(self):
        """Проверка добавления карты."""

        old_cards_pk = [pk for pk in
                        Card.objects
                        .values_list('pk', flat=True)]

        response = self.auth_client.post(
            self.CARDS_URL,
            {
                'name': 'Test Card',
                'shop': self.shop.id,
                'image': self.UPLOADED_GIF.open(),
                'card_number': '123456789012',
                'barcode_number': '123456789012',
                'encoding_type': 'ean-13',
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_card = Card.objects.exclude(pk__in=old_cards_pk).last()
        self.assert_user_has_new_card(new_card.pk)

    def test_card_create_with_new_shop(self):
        """Проверка создания карты с новым магазином."""
        old_cards_pk = [pk for pk in
                        Card.objects
                        .values_list('pk', flat=True)]

        response = self.auth_client.post(
            self.CARDS_URL + 'new-shop/',
            {
                'shop': {
                    'name': 'New Shop',
                },
                'name': 'Test Card with New Shop',
                'card_number': '157',
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['shop']['name'], 'New Shop')
        self.assertEqual(response.data['name'], 'Test Card with New Shop')

        new_card = Card.objects.exclude(pk__in=old_cards_pk).last()
        self.assert_user_has_new_card(new_card.pk)

    def test_card_edit_by_owner(self):
        """Проверка редактирования карты владельцем."""

        response = self.auth_client.patch(
            self.CARD_DETAIL_URL,
            {
                'name': 'New name',
                'shop': self.shop.id,
                'image': self.UPLOADED_GIF.open(),
                'card_number': '123456789012',
                'barcode_number': '123456789012',
                'encoding_type': 'ean-13',
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.card.refresh_from_db()
        self.assertEqual(self.card.name, 'New name')

    def test_card_edit_by_not_owner(self):
        """Проверка редактирования карты не владельцем."""

        response = self.auth_client.patch(
            reverse(
                'api:card-detail',
                kwargs={'pk': self.card_user_not_own.pk}),
            {
                'name': 'New name',
                'shop': self.shop.id,
                'image': self.UPLOADED_GIF.open(),
                'card_number': '123456789012',
                'barcode_number': '123456789012',
                'encoding_type': 'ean-13',
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_card_delete_by_owner(self):
        """Проверка удаления карты ее владельцем."""

        response = self.auth_client.delete(self.CARD_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"Message": "Карта успешно удалена."})
        self.assertFalse(
            UserCards.objects.filter(
                user=self.user, card__pk=self.card.pk).exists(),
            'У пользователя не удалилась карта.'
        )
        self.assertFalse(
            Card.objects.filter(pk=self.card.pk).exists(),
            'Карта не удалилась.'
        )

    def test_card_delete_by_not_owner(self):
        """Проверка удаления карты не ее владельцем."""

        response = self.auth_client.delete(reverse(
            'api:card-detail',
            kwargs={'pk': self.card_user_not_own.pk}
        ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"Message": "Карта успешно удалена."})
        self.assertFalse(
            UserCards.objects.filter(
                user=self.user, card__pk=self.card_user_not_own.pk).exists(),
            'У пользователя из списка не удалилась карта.'
        )
        self.assertTrue(
            Card.objects.filter(pk=self.card_user_not_own.pk).exists(),
            'Карту может удалить не ее владелец.'
        )

    def test_card_statistics(self):
        """Проверка увеличения счетчика использования карты."""

        response = self.auth_client.patch(
            reverse(
                'api:card-statistics',
                kwargs={'pk': self.card.pk}
            ),
            {
                'usage_counter': "157",
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            UserCards.objects.filter(
                user=self.user, card__pk=self.card.pk).first().usage_counter,
            157
        )

    def test_cards_favorite_list_count(self):
        """Проверка количества карт в избранных."""

        response = self.auth_client.get(
            self.CARDS_URL + 'favorites/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.CARDS_USER_FAV)

    def test_cards_favorite_add_remove(self):
        """Проверка добавления и удаления карты из избранного."""
        url = reverse(
            'api:card-detail',
            kwargs={'pk': f'{self.card_user_not_fav.id}'}
        ) + 'favorite/'

        response = self.auth_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            UserCards.objects.get(
                user=self.user, card=self.card_user_not_fav).favourite,
            'Карта не добавилась в избранное.'
        )

        response = self.auth_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            UserCards.objects.get(
                user=self.user, card=self.card_user_not_fav).favourite,
            'Карта не удалилась из избранного.'
        )

    def test_shops_list_accessibility_for_guest(self):
        """Проверка выдачи списка проверенных магазинов гостю."""

        response = self.guest_client.get(reverse('api:shop-list'))
        self.assertEqual(len(response.data), self.SHOPS_VERIFY)

    def test_group_list_accessibility_for_guest(self):
        """Проверка выдачи списка категорий гостю."""

        response = self.guest_client.get(reverse('api:group-list'))
        self.assertEqual(len(response.data), self.GROUPS)


class ShopEditTestCase(APIShopEditTests):
    """Проверка редактирования неверифицированного магазина."""

    def test_unvalidated_shop_edit(self):
        """Пользователь, создавший магазин, может его редактировать."""
        response = self.auth_client.patch(
            reverse(
                'api:shop-detail',
                kwargs={'pk': f'{self.shop_unvalidated.id}'},
            ),
            {
                'name': 'New shop name',
                'group': f'{self.group.id}'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.shop_unvalidated.refresh_from_db()
        self.assertEqual(self.shop_unvalidated.name, 'New shop name')
        group = self.shop_unvalidated.group.all()[0]
        self.assertEqual(group, self.group)

    def test_unvalidated_friends_shop_not_edit(self):
        """Пользователь не может редактировать магазин расшаренной карты."""

        response = self.auth_client.patch(
            reverse(
                'api:shop-detail',
                kwargs={'pk': f'{self.shop_unvalidated_from_friends_card.id}'},
            ),
            {
                'name': 'New shop name',
                'group': f'{self.group.id}'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_validated_shop_not_edit(self):
        """Пользователь не может редактировать предустановленный магазин."""

        response = self.auth_client.patch(
            reverse(
                'api:shop-detail',
                kwargs={'pk': f'{self.shop_validated.id}'},
            ),
            {
                'name': 'New shop name',
                'group': f'{self.group.id}'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
