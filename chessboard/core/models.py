from django.db import models


class Piece(models.Model):
    class Color(models.IntegerChoices):
        BLACK = 1, 'Black'
        WHITE = 2, 'White'

    class Type(models.IntegerChoices):
        KNIGHT = 1, 'Knight'
        OTHER = 2, 'Other piece'

    color = models.IntegerField(choices=Color.choices)
    type = models.IntegerField(choices=Type.choices)

    class Meta:
        verbose_name = 'Piece'
        verbose_name_plural = 'Pieces'
