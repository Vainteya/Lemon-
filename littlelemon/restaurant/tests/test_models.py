from datetime import datetime, timezone

from django.test import TestCase

from restaurant.models import Booking, MenuItem


class MenuItemTest(TestCase):
    def test_get_item(self):
        item = MenuItem.objects.create(title="IceCream", price=80, inventory=100)
        self.assertEqual(str(item), "IceCream : 80")

    def test_str_after_reload_uses_decimal_places(self):
        item = MenuItem.objects.create(title="Greek Salad", price=12.5, inventory=20)
        item.refresh_from_db()
        self.assertEqual(str(item), "Greek Salad : 12.50")


class BookingTest(TestCase):
    def test_default_number_of_guests(self):
        booking = Booking.objects.create(
            name="Alice",
            booking_date=datetime(2026, 11, 1, 19, 30, tzinfo=timezone.utc),
        )
        self.assertEqual(booking.no_of_guests, 6)

    def test_str_contains_name_and_date(self):
        when = datetime(2026, 11, 1, 19, 30, tzinfo=timezone.utc)
        booking = Booking.objects.create(name="Alice", no_of_guests=2, booking_date=when)
        self.assertEqual(str(booking), f"Alice : {when}")
