import pytest
from rest_framework import status
from rest_framework.reverse import reverse

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
    payload = {
        'color': Piece.Color.BLACK,
        'type': Piece.Type.KNIGHT,
    }
    r_json = api_client.post(reverse('Core:Piece-list'), data=payload).json()

    assert r_json['id']


@pytest.mark.django_db
def test_piece_movements_action__without_origin(
        api_client, black_knight_piece
):
    r = api_client.get(reverse('Core:Piece-movements', kwargs={'pk': 1}))

    assert r.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_piece_movements_action__with_origin(api_client, black_knight_piece):
    payload = {'origin': 'a8'}

    r = api_client.get(
        reverse('Core:Piece-movements', kwargs={'pk': 1}), data=payload
    )

    assert r.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_piece_movements_action__has_movements(api_client, black_knight_piece):
    payload = {'origin': 'a8'}

    r_json = api_client.get(
        reverse('Core:Piece-movements', kwargs={'pk': black_knight_piece.id}),
        data=payload,
    ).json()

    assert 'movements' in r_json


@pytest.mark.django_db
def test_piece_movements_action__movements_is_a_list(
        api_client, black_knight_piece
):
    payload = {'origin': 'a8'}

    r_json = api_client.get(
        reverse('Core:Piece-movements', kwargs={'pk': black_knight_piece.id}),
        data=payload,
    ).json()

    assert isinstance(r_json['movements'], list)


@pytest.mark.django_db
def test_piece_movements_action__other_piece_without_movements(
        api_client, black_piece_of_another_type
):
    payload = {'origin': 'a8'}

    r_json = api_client.get(
        reverse(
            'Core:Piece-movements',
            kwargs={'pk': black_piece_of_another_type.id},
        ),
        data=payload,
    ).json()

    assert r_json['movements'] == []


@pytest.mark.django_db
def test_piece_movements_action__knight_piece_with_movements(
        api_client, black_knight_piece
):
    payload = {'origin': 'a8'}

    r_json = api_client.get(
        reverse('Core:Piece-movements', kwargs={'pk': black_knight_piece.id}),
        data=payload,
    ).json()

    assert len(r_json['movements'])
