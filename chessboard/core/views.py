from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.facade import location_in_the_board, next_moves_of_the_piece
from core.models import Piece
from core.serializers import PieceSerializer


def hello_world(request):
    return JsonResponse({'hello': 'world'})


class PieceViewSet(viewsets.ModelViewSet):
    queryset = Piece.objects.all().order_by('color')
    serializer_class = PieceSerializer

    @action(detail=True, methods=['get'])
    def moves(self, request, pk=None):
        piece = get_object_or_404(Piece, pk=pk)

        origin = request.query_params.get('origin')
        if not origin or not location_in_the_board(origin):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(next_moves_of_the_piece(piece=piece, origin=origin))
