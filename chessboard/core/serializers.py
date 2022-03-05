from rest_framework import serializers

from core.facade import DEFAULT_BOARD_SIZE, location_in_the_board
from core.models import Piece


class PieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Piece
        fields = ['id', 'color', 'type']


class PieceMovesRequestSerializer(serializers.Serializer):
    origin = serializers.CharField(
        help_text='Piece origin location in algebraic notation.',
        min_length=2,
        trim_whitespace=True,
    )
    board_cols = serializers.IntegerField(
        help_text='Number of columns on the chess board',
        default=DEFAULT_BOARD_SIZE,
        min_value=4,
        required=False,
    )
    board_rows = serializers.IntegerField(
        help_text='Number of rows on the chess board',
        default=DEFAULT_BOARD_SIZE,
        min_value=4,
        required=False,
    )

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def validate(self, attrs):
        if not location_in_the_board(
            location=attrs['origin'],
            board_cols=attrs['board_cols'],
            board_rows=attrs['board_rows'],
        ):
            raise serializers.ValidationError(
                'Invalid piece origin location. Did you enter it as '
                'algebraic notation?'
            )

        return attrs
