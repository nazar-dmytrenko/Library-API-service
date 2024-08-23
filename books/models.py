from django.db import models
from django.core.validators import MinValueValidator

from enum import Enum


class BookCover(Enum):
    HARD = "HARD"
    SOFT = "SOFT"


class Book(models.Model):
    title = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255)
    cover = models.CharField(
        max_length=10, choices=[(cover.name, cover.name) for cover in BookCover]
    )
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    daily_fee = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.title
