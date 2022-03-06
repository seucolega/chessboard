from django.db import models


class Piece(models.Model):
    class Color(models.TextChoices):
        BLACK = 'B', 'Black'
        WHITE = 'W', 'White'

    class Type(models.TextChoices):
        KING = 'K', 'King'
        QUEEN = 'Q', 'Queen'
        ROOK = 'R', 'Rook'
        BISHOP = 'B', 'Bishop'
        KNIGHT = 'N', 'Knight'
        PAWN = 'P', 'Pawn'

    color = models.CharField(choices=Color.choices, max_length=1)
    type = models.CharField(choices=Type.choices, max_length=1)

    class Meta:
        verbose_name = 'Piece'
        verbose_name_plural = 'Pieces'
        ordering = ['color', 'type']

    def __str__(self):
        return ', '.join(
            (
                str(self.pk),
                self.Color(self.color).label,
                self.Type(self.type).label,
            )
        )
