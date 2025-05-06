from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Vehicle(models.Model):

    wheel = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        db_table = "vehicles"
