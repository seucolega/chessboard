from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.facade import next_moves_of_the_piece
from core.models import Piece
from core.serializers import PieceMovesRequestSerializer, PieceSerializer, \
    PieceMovesResponseSerializer


def hello_world(request):
    return JsonResponse({'hello': 'world'})


class PieceViewSet(viewsets.ModelViewSet):
    queryset = Piece.objects.all().order_by('color')
    serializer_class = PieceSerializer

    @extend_schema(
        summary='Next moves of the piece',
        parameters=[PieceMovesRequestSerializer],
        request=PieceMovesRequestSerializer,
        responses=PieceMovesResponseSerializer
    )
    @action(detail=True, methods=['get'], name='Next moves of the piece')
    def moves(self, request, pk: int = None):
        """
        Returns possible moves of the piece from the informed origin.
        """
        piece = get_object_or_404(Piece, pk=pk)

        serializer = PieceMovesRequestSerializer(data=request.query_params)
        if serializer.is_valid():
            data = next_moves_of_the_piece(
                piece=piece,
                origin=serializer.validated_data['origin'],
                board_cols=serializer.validated_data['board_cols'],
                board_rows=serializer.validated_data['board_rows'],
            )

            serializer = PieceMovesResponseSerializer(data=data)
            serializer.is_valid()

            return Response(serializer.validated_data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
