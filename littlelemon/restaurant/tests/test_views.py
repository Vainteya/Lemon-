from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from restaurant.models import Booking, MenuItem
from restaurant.serializers import BookingSerializer, MenuItemSerializer


class IndexViewTest(TestCase):
    def test_home_page_renders_index_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class MenuViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='staff', password='staff-pass!')
        MenuItem.objects.create(title="IceCream", price=80, inventory=100)
        MenuItem.objects.create(title="Bruschetta", price=7.5, inventory=50)
        MenuItem.objects.create(title="Lemon Dessert", price=6, inventory=30)

    def test_getall(self):
        response = self.client.get('/api/menu-items/')
        expected = MenuItemSerializer(MenuItem.objects.all(), many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected)

    def test_get_single_item(self):
        item = MenuItem.objects.get(title="Bruschetta")
        response = self.client.get(f'/api/menu-items/{item.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), MenuItemSerializer(item).data)

    def test_anonymous_cannot_modify(self):
        item = MenuItem.objects.get(title="IceCream")
        create = self.client.post(
            '/api/menu-items/', {'title': 'X', 'price': '1.00', 'inventory': 1}, format='json'
        )
        update = self.client.patch(f'/api/menu-items/{item.pk}/', {'inventory': 1}, format='json')
        delete = self.client.delete(f'/api/menu-items/{item.pk}/')
        self.assertEqual(create.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(update.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(delete.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(MenuItem.objects.filter(pk=item.pk).exists())

    def test_rejects_invalid_values(self):
        self.client.force_authenticate(user=self.user)
        for bad in (
            {'title': 'X', 'price': '-1.00', 'inventory': 1},
            {'title': 'X', 'price': '1.00', 'inventory': -1},
            {'title': 'X', 'price': '1.00', 'inventory': 40000},
        ):
            with self.subTest(payload=bad):
                response = self.client.post('/api/menu-items/', bad, format='json')
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(MenuItem.objects.count(), 3)

    def test_create_item(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/api/menu-items/',
            {'title': 'Greek Salad', 'price': '12.99', 'inventory': 15},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(MenuItem.objects.filter(title='Greek Salad').exists())

    def test_update_item(self):
        self.client.force_authenticate(user=self.user)
        item = MenuItem.objects.get(title="IceCream")
        response = self.client.patch(
            f'/api/menu-items/{item.pk}/', {'inventory': 5}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item.refresh_from_db()
        self.assertEqual(item.inventory, 5)

    def test_delete_item(self):
        self.client.force_authenticate(user=self.user)
        item = MenuItem.objects.get(title="Lemon Dessert")
        response = self.client.delete(f'/api/menu-items/{item.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(MenuItem.objects.filter(pk=item.pk).exists())


class BookingViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='tester', password='s3cret-pass!')
        self.token = Token.objects.create(user=self.user)
        self.booking = Booking.objects.create(
            name='Alice', no_of_guests=4, booking_date='2026-11-01T19:30:00Z'
        )

    def test_requires_authentication(self):
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_with_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/bookings/')
        expected = BookingSerializer(Booking.objects.all(), many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected)

    def test_create_with_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(
            '/api/bookings/',
            {'name': 'Bob', 'no_of_guests': 2, 'booking_date': '2026-12-24T20:00:00Z'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Booking.objects.filter(name='Bob').exists())

    def test_rejects_fewer_than_one_guest(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        for guests in (0, -4):
            with self.subTest(no_of_guests=guests):
                response = self.client.post(
                    '/api/bookings/',
                    {'name': 'Z', 'no_of_guests': guests, 'booking_date': '2026-12-24T20:00:00Z'},
                    format='json',
                )
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Booking.objects.count(), 1)

    def test_delete_with_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.delete(f'/api/bookings/{self.booking.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Booking.objects.filter(pk=self.booking.pk).exists())


class UserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            username='admin', password='admin-pass!', email='admin@example.com'
        )

    def test_regular_user_is_forbidden(self):
        user = User.objects.create_user(username='regular', password='regular-pass!')
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_lists_users(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            [{
                'url': f'http://testserver/api/users/{self.admin.pk}/',
                'username': 'admin',
                'email': 'admin@example.com',
                'groups': [],
            }],
        )


class AuthFlowTest(TestCase):
    def test_register_and_login_returns_token(self):
        client = APIClient()
        register = client.post(
            '/auth/users/',
            {'username': 'newuser', 'password': 'LemonPass#2026', 'email': 'new@example.com'},
            format='json',
        )
        self.assertEqual(register.status_code, status.HTTP_201_CREATED)

        login = client.post(
            '/auth/token/login/',
            {'username': 'newuser', 'password': 'LemonPass#2026'},
            format='json',
        )
        self.assertEqual(login.status_code, status.HTTP_200_OK)
        self.assertIn('auth_token', login.json())
