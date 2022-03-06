import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from core import facade
from core.models import Piece


@pytest.mark.django_db
def test_hello_world__exists(api_client):
    r = api_client.get(reverse('Core:Hello World'))

    assert r.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_piece__list(api_client):
    r = api_client.get(reverse('Core:Piece-list'))

    assert r.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_piece__list_with_a_piece(api_client, black_knight_piece):
    r_json = api_client.get(reverse('Core:Piece-list')).json()

    assert len(r_json) == 1


@pytest.mark.django_db
def test_piece__list_with_a_piece_and_id_attr(api_client, black_knight_piece):
    r_json = api_client.get(reverse('Core:Piece-list')).json()

    assert r_json[0]['id']


@pytest.mark.django_db
def test_piece__create(api_client):
    payload = {
        'color': Piece.Color.BLACK,
        'type': Piece.Type.KNIGHT,
    }

    r = api_client.post(reverse('Core:Piece-list'), data=payload)

    assert r.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_piece__create_with_id_attr(api_client):
    payload = {'color': Piece.Color.BLACK, 'type': Piece.Type.KNIGHT}

    r_json = api_client.post(reverse('Core:Piece-list'), data=payload).json()

    assert r_json['id']


@pytest.mark.django_db
def test_piece_moves_action__with_non_existent_piece(api_client):
    r = api_client.get(reverse('Core:Piece-moves', kwargs={'pk': 1}))

    assert r.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_piece_moves_action__without_origin(api_client, black_knight_piece):
    r = api_client.get(reverse('Core:Piece-moves', kwargs={'pk': 1}))

    assert r.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_piece_moves_action__with_origin(api_client, black_knight_piece):
    payload = {'origin': 'c6'}

    r = api_client.get(
        reverse('Core:Piece-moves', kwargs={'pk': 1}), data=payload
    )

    assert r.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_piece_moves_action__has_first_moves(api_client, black_knight_piece):
    payload = {'origin': 'c6'}

    r_json = api_client.get(
        reverse('Core:Piece-moves', kwargs={'pk': black_knight_piece.id}),
        data=payload,
    ).json()

    assert 'first' in r_json


@pytest.mark.django_db
def test_piece_moves_action__first_moves_is_a_list(
    api_client, black_knight_piece
):
    payload = {'origin': 'c6'}

    r_json = api_client.get(
        reverse('Core:Piece-moves', kwargs={'pk': black_knight_piece.id}),
        data=payload,
    ).json()

    assert isinstance(r_json['first'], list)


@pytest.mark.django_db
def test_piece_moves_action__other_piece_has_no_moves(
    api_client, black_king_piece
):
    payload = {'origin': 'c6'}

    r_json = api_client.get(
        reverse(
            'Core:Piece-moves',
            kwargs={'pk': black_king_piece.id},
        ),
        data=payload,
    ).json()

    assert r_json['first'] == []


@pytest.mark.django_db
def test_piece_moves_action__knight_piece_with_first_moves(
    api_client, black_knight_piece
):
    payload = {'origin': 'c6'}

    r_json = api_client.get(
        reverse('Core:Piece-moves', kwargs={'pk': black_knight_piece.id}),
        data=payload,
    ).json()

    assert len(r_json['first'])


@pytest.mark.django_db
def test_piece_moves_action__knight_piece_first_moves(
    api_client, black_knight_piece
):
    payload = {'origin': 'h1'}

    r_json = api_client.get(
        reverse('Core:Piece-moves', kwargs={'pk': black_knight_piece.id}),
        data=payload,
    ).json()

    assert set(r_json['first']) == {'f2', 'g3'}


@pytest.mark.django_db
def test_piece_moves_action__has_second_moves(api_client, black_knight_piece):
    payload = {'origin': 'c6'}

    r_json = api_client.get(
        reverse('Core:Piece-moves', kwargs={'pk': black_knight_piece.id}),
        data=payload,
    ).json()

    assert 'second' in r_json


@pytest.mark.django_db
def test_piece_moves_action__second_moves_is_a_dict(
    api_client, black_knight_piece
):
    payload = {'origin': 'c6'}

    r_json = api_client.get(
        reverse('Core:Piece-moves', kwargs={'pk': black_knight_piece.id}),
        data=payload,
    ).json()

    assert isinstance(r_json['second'], dict)


@pytest.mark.django_db
def test_piece_moves_action__other_piece_has_no_second_moves(
    api_client, black_king_piece
):
    payload = {'origin': 'c6'}

    r_json = api_client.get(
        reverse(
            'Core:Piece-moves',
            kwargs={'pk': black_king_piece.id},
        ),
        data=payload,
    ).json()

    assert r_json['second'] == {}


@pytest.mark.django_db
def test_piece_moves_action__knight_piece_with_second_moves(
    api_client, black_knight_piece
):
    payload = {'origin': 'c6'}

    r_json = api_client.get(
        reverse('Core:Piece-moves', kwargs={'pk': black_knight_piece.id}),
        data=payload,
    ).json()

    assert len(r_json['second'].keys())


@pytest.mark.django_db
def test_piece_moves_action__knight_piece_second_moves_grouped_by_the_first(
    api_client, black_knight_piece
):
    payload = {'origin': 'h1'}

    r_json = api_client.get(
        reverse('Core:Piece-moves', kwargs={'pk': black_knight_piece.id}),
        data=payload,
    ).json()

    assert set(r_json['second'].keys()) == {'f2', 'g3'}


@pytest.mark.django_db
def test_piece_moves_action__knight_piece_second_moves__from_f2(
    api_client, black_knight_piece
):
    payload = {'origin': 'h1'}

    r_json = api_client.get(
        reverse('Core:Piece-moves', kwargs={'pk': black_knight_piece.id}),
        data=payload,
    ).json()

    assert set(r_json['second']['f2']) == {'h3', 'g4', 'e4', 'd3', 'd1'}


@pytest.mark.django_db
def test_piece_moves_action__knight_piece_second_moves__from_g3(
    api_client, black_knight_piece
):
    payload = {'origin': 'h1'}

    r_json = api_client.get(
        reverse('Core:Piece-moves', kwargs={'pk': black_knight_piece.id}),
        data=payload,
    ).json()

    assert set(r_json['second']['g3']) == {'h5', 'f5', 'e4', 'e2', 'f1'}


@pytest.mark.django_db
def test_piece_moves_action__knight_piece_second_moves__from_b3_on_a_4x4_board(
    api_client, black_knight_piece
):
    payload = {'origin': 'a1', 'board_cols': 4, 'board_rows': 4}

    r_json = api_client.get(
        reverse('Core:Piece-moves', kwargs={'pk': black_knight_piece.id}),
        data=payload,
    ).json()

    assert set(r_json['second']['b3']) == {'d4', 'd2', 'c1'}


@pytest.mark.django_db
def test_piece_moves_action__knight_piece_second_moves__from_c2_on_a_4x4_board(
    api_client, black_knight_piece
):
    payload = {'origin': 'a1', 'board_cols': 4, 'board_rows': 4}

    r_json = api_client.get(
        reverse('Core:Piece-moves', kwargs={'pk': black_knight_piece.id}),
        data=payload,
    ).json()

    assert set(r_json['second']['c2']) == {'d4', 'b4', 'a3'}


@pytest.mark.django_db
def test_piece_moves_action__piece_on_i1_is_out_off_the_board(
    api_client, black_knight_piece
):
    payload = {'origin': 'i1'}

    r = api_client.get(
        reverse('Core:Piece-moves', kwargs={'pk': black_knight_piece.id}),
        data=payload,
    )

    assert r.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_piece_moves_action__piece_on_h9_is_out_off_the_board(
    api_client, black_knight_piece
):
    payload = {'origin': 'h9'}

    r = api_client.get(
        reverse('Core:Piece-moves', kwargs={'pk': black_knight_piece.id}),
        data=payload,
    )

    assert r.status_code == status.HTTP_400_BAD_REQUEST


def test_location_is_inside_chessboard__a1_is_on_the_board():
    assert facade.location_in_the_board('a1') is True


def test_location_is_inside_chessboard__h8_is_on_the_board():
    assert facade.location_in_the_board('h8') is True


def test_location_is_inside_chessboard__i1_is_off_the_board():
    assert facade.location_in_the_board('i1') is False


def test_location_is_inside_chessboard__h9_is_off_the_board():
    assert facade.location_in_the_board('h9') is False


def test_possible_knight_moves__from_d4():
    result = facade.possible_knight_moves('d4')

    assert set(result) == {'b5', 'c6', 'e6', 'f5', 'f3', 'e2', 'c2', 'b3'}


def test_possible_knight_moves__from_h1():
    result = facade.possible_knight_moves('h1')

    assert set(result) == {'f2', 'g3'}


def test_possible_knight_moves__from_b3_on_a_4x4_board():
    result = facade.possible_knight_moves('b3', board_cols=4, board_rows=4)

    assert set(result) == {'c1', 'd2', 'a1', 'd4'}


def test_possible_knight_moves__from_c2_on_a_4x4_board():
    result = facade.possible_knight_moves('c2', board_cols=4, board_rows=4)

    assert set(result) == {'a3', 'b4', 'd4', 'a1'}


@pytest.mark.django_db
def test_piece_title(api_client, black_knight_piece):
    assert str(black_knight_piece) == '1, Black, Knight'
