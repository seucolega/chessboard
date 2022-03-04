from rest_framework import serializers

from core.models import Piece


class PieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Piece
        fields = ['id', 'color', 'type']
