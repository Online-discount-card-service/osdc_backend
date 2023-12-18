from django.contrib.auth import get_user_model
from django.core import mail
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

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
            'shared_by', 'pub_date'
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
        self.assertEqual(response.data, {"message": "Карта успешно удалена."})
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
        self.assertEqual(response.data, {"message": "Карта успешно удалена."})
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
                'usage_counter': '157',
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

    def test_card_share(self):
        """Проверка возможности поделиться картой внутри приложения."""

        email = self.another_user.email
        url = reverse(
            'api:card-share',
            kwargs={'pk': f'{self.card_user_own.id}'}
        )
        response = self.auth_client.post(url, {'email': email}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(UserCards.objects.filter(
            user=self.another_user,
            card=self.card_user_own
        ).exists(), 'Картой не удалось поделиться')
        self.assertFalse(UserCards.objects.get(
            user=self.another_user,
            card=self.card_user_own).owner,
            'У того, с кем делились картой, её не появилось в списке карт.')

    def test_double_card_share(self):
        """Проверка невозможности поделиться каротй повторно."""
        UserCards.objects.create(
            user=self.another_user,
            card=self.card_user_own
        )
        email = self.another_user.email
        url = reverse(
            'api:card-share',
            kwargs={'pk': f'{self.card_user_own.id}'}
        )
        response = self.auth_client.post(url, {'email': email}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_self_share(self):
        """Проверка невозможности поделиться картой с самим собой."""
        email_of_user_who_share = self.user.email
        url = reverse(
            'api:card-share',
            kwargs={'pk': f'{self.card_user_own.id}'}
        )
        response = self.auth_client.post(
            url,
            {'email': email_of_user_who_share},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_card_share_with_non_user(self):
        """Проверка возможности отправить приглашение на е-мейл."""

        url = reverse(
            'api:card-share',
            kwargs={'pk': f'{self.card_user_own.id}'}
        )
        email = self.EMAIL_NOT_OF_A_USER
        response = self.auth_client.post(url, {'email': email}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(mail.outbox),
            1,
            'Не удалось отправить письмо-приглашение.'
        )
        self.assertIn(
            'С вами хотят поделитсья скидочной картой на сайте',
            mail.outbox[0].subject
        )
        self.assertIn(email, mail.outbox[0].recipients())
        context = mail.outbox[0].get_context_data()
        self.assertEqual(context['card'], self.card_user_own)


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


class CustomizedDjoserTestCase(APITests):
    """Проверка кастомизированных ручек Djoser."""

    def test_unactivated_user_can_login(self):
        """Неактивированный пользователь может залогиниться."""

        response = self.client.post(
            reverse('api:login'),
            {'email': self.unactivated_user.email,
             'password': 'TestPass2'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_recovery(self):
        """Пользователь может запросить восстановление пароля."""

        users_phone = self.user.phone_number
        response = self.client.post(
            reverse('api:user-reset-password'),
            {
                'email': self.user.email,
                'phone_last_digits': users_phone[-4:]
            },
            format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            'Не удалось отправить запрос на смену пароля.'
        )

    def check_activation(self, mail_context, email):
        uid = mail_context['uid']
        token = mail_context['token']
        user = User.objects.get(email=email)
        unactivated_client = APIClient()
        unactivated_client.force_authenticate(user=user)
        response = unactivated_client.post(
            reverse('api:user-activation'),
            {
                'uid': uid,
                'token': token
            }
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        user.refresh_from_db()
        self.assertTrue(user.is_active, 'Не удалось активировать почту.')

    def test_email_activation(self):
        """Пользователь получает email для активации."""

        email = 'testemail@test.ru'
        response = self.client.post(
            reverse('api:user-list'),
            {
                'email': email,
                'name': 'test',
                'password': 'Password1',
                'phone_number': '9123456789'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            len(mail.outbox),
            1,
            'Не удалось отправить письмо для активации.'
        )
        self.assertIn(email, mail.outbox[0].recipients())
        mail_context = mail.outbox[0].get_context_data()
        self.assertIn('uid', mail_context)
        self.assertIn('token', mail_context)
        self.check_activation(mail_context=mail_context, email=email)

    def test_user_can_activate_email(self):
        """Пользователь может активировать почту."""

        self.inactive_auth_client.post(reverse('api:user-resend-activation'))
        mail_context = mail.outbox[0].get_context_data()
        email = self.unactivated_user.email
        self.check_activation(mail_context=mail_context, email=email)
