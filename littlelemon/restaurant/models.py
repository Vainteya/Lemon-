from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Booking(models.Model):
    name = models.CharField(max_length=255)
    no_of_guests = models.IntegerField(default=6, validators=[MinValueValidator(1)])
    booking_date = models.DateTimeField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.name} : {self.booking_date}'


class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))]
    )
    # Upper bound matches MySQL's SMALLINT so every backend rejects the same values.
    inventory = models.SmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(32767)]
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.title} : {str(self.price)}'
