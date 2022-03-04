import pytest

from core.models import Piece


@pytest.fixture
def black_knight_piece() -> Piece:
    return Piece.objects.create(
        type=Piece.Type.KNIGHT, color=Piece.Color.BLACK
    )


@pytest.fixture
def black_piece_of_another_type() -> Piece:
    return Piece.objects.create(type=Piece.Type.OTHER, color=Piece.Color.BLACK)
