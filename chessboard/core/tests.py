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
def test_piece_moves_action__other_piece_without_moves(
    api_client, black_piece_of_another_type
):
    payload = {'origin': 'c6'}

    r_json = api_client.get(
        reverse(
            'Core:Piece-moves',
            kwargs={'pk': black_piece_of_another_type.id},
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
def test_piece_moves_action__has_second_moves__first(
    api_client, black_knight_piece
):
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
def test_piece_moves_action__other_piece_without_moves__second(
    api_client, black_piece_of_another_type
):
    payload = {'origin': 'c6'}

    r_json = api_client.get(
        reverse(
            'Core:Piece-moves',
            kwargs={'pk': black_piece_of_another_type.id},
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


def test_location_is_inside_chessboard__on_the_board_1():
    assert facade.location_in_the_board('a1') is True


def test_location_is_inside_chessboard__on_the_board_2():
    assert facade.location_in_the_board('h8') is True


def test_location_is_inside_chessboard__off_the_board_1():
    assert facade.location_in_the_board('i1') is False


def test_location_is_inside_chessboard__off_the_board_2():
    assert facade.location_in_the_board('h9') is False


def test_possible_knight_moves():
    result = facade.possible_knight_moves('d4')

    expected = ['b5', 'c6', 'e6', 'f5', 'f3', 'e2', 'c2', 'b3']

    assert set(result) == set(expected)


def test_possible_knight_moves__2():
    result = facade.possible_knight_moves('h1')

    expected = ['f2', 'g3']

    assert set(result) == set(expected)
