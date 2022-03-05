import re
from typing import Dict, List, Tuple, Union

from core.models import Piece

BOARD_SIZE = 8


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


def board_col_and_row() -> Tuple[int, int]:
    return BOARD_SIZE, BOARD_SIZE


def location_in_the_board(location: str) -> bool:
    board_cols, board_rows = board_col_and_row()

    col, row = algebraic_notation_to_col_and_row(location)

    return col <= board_cols and row <= board_rows


def algebraic_notation_to_col_and_row(location: str) -> Tuple[int, int]:
    return letter_to_int(only_alphas(location)), int(only_numbers(location))


def col_and_row_to_algebraic_notation(col: int, row: int) -> str:
    return int_to_letter(col) + str(row)


def possible_knight_moves(origin: str) -> List[str]:
    result = []
    board_cols, board_rows = board_col_and_row()
    origin_col, origin_row = algebraic_notation_to_col_and_row(origin)

    # All possible moves of a knight
    # TODO: Check possible moves for different boards
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
    piece: Piece, origin: str
) -> Dict[str, Union[List[str], Dict[str, List[str]]]]:
    result = {'first': [], 'second': {}}

    if piece.type is Piece.Type.KNIGHT.value:
        result['first'] = possible_knight_moves(origin)
        result['second'] = {
            location: possible_knight_moves(location)
            for location in result['first']
        }

    return result
