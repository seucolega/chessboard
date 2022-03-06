from django.db import models


class Piece(models.Model):
    class Color(models.TextChoices):
        BLACK = 'B', 'Black'
        WHITE = 'W', 'White'

    class Type(models.TextChoices):
        KNIGHT = 'K', 'Knight'
        OTHER = 'O', 'Other piece'

    color = models.CharField(choices=Color.choices, max_length=1)
    type = models.CharField(choices=Type.choices, max_length=1)

    class Meta:
        verbose_name = 'Piece'
        verbose_name_plural = 'Pieces'
