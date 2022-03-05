import re
from typing import Dict, List, Tuple, Union

from core.models import Piece

DEFAULT_BOARD_SIZE = 8


def only_numbers(numbers: str) -> str:
    return (
        ''.join(re.findall(r'\d+', numbers))
        if isinstance(numbers, str)
        else ''
    )


def only_alphas(text: str) -> str:
    return (
        ''.join(e for e in text if e.isalpha())
        if isinstance(text, str)
        else ''
    )


def letter_to_int(letter: str) -> int:
    return ord(letter) - 96


def int_to_letter(number: int) -> str:
    return chr(number + 96)


def location_in_the_board(
    location: str,
    board_cols: int = DEFAULT_BOARD_SIZE,
    board_rows: int = DEFAULT_BOARD_SIZE,
) -> bool:
    col, row = algebraic_notation_to_col_and_row(location)

    return col <= board_cols and row <= board_rows


def algebraic_notation_to_col_and_row(location: str) -> Tuple[int, int]:
    return letter_to_int(only_alphas(location)), int(only_numbers(location))


def col_and_row_to_algebraic_notation(col: int, row: int) -> str:
    return int_to_letter(col) + str(row)


def possible_knight_moves(
    origin: str,
    board_cols: int = DEFAULT_BOARD_SIZE,
    board_rows: int = DEFAULT_BOARD_SIZE,
) -> List[str]:
    result = []
    origin_col, origin_row = algebraic_notation_to_col_and_row(origin)

    # All possible moves of a knight
    col_moves = [2, 1, -1, -2, -2, -1, 1, 2]
    row_moves = [1, 2, 2, 1, -1, -2, -2, -1]

    # Check if each possible move is valid or not
    for col_move, row_move in zip(col_moves, row_moves):
        # Position of knight after move
        col = origin_col + col_move
        row = origin_row + row_move

        if 0 < col <= board_rows and 0 < row <= board_cols:
            result.append(col_and_row_to_algebraic_notation(col=col, row=row))

    return result


def next_moves_of_the_piece(
    piece: Piece, origin: str, board_cols: int, board_rows: int
) -> Dict[str, Union[List[str], Dict[str, List[str]]]]:
    result = {'first': [], 'second': {}}

    if piece.type is Piece.Type.KNIGHT.value:
        result['first'] = possible_knight_moves(
            origin=origin, board_cols=board_cols, board_rows=board_rows
        )
        for location in result['first']:
            moves = possible_knight_moves(
                origin=location, board_cols=board_cols, board_rows=board_rows
            )
            moves.remove(origin)
            result['second'][location] = moves

    return result
