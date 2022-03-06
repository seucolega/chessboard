from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    OpenApiExample,
    extend_schema,
    extend_schema_view,
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.facade import next_moves_of_the_piece
from core.models import Piece
from core.serializers import (
    PieceMovesRequestSerializer,
    PieceMovesResponseSerializer,
    PieceSerializer,
)


def hello_world(request):
    return JsonResponse({'hello': 'world'})


@extend_schema_view(
    list=extend_schema(summary='List'),
    create=extend_schema(summary='Create'),
    retrieve=extend_schema(summary='Retrieve'),
    update=extend_schema(summary='Update'),
    partial_update=extend_schema(summary='Partial update'),
    destroy=extend_schema(summary='Destroy'),
)
class PieceViewSet(viewsets.ModelViewSet):
    queryset = Piece.objects.all().order_by('color')
    serializer_class = PieceSerializer

    @extend_schema(
        summary='Next moves',
        parameters=[PieceMovesRequestSerializer],
        request=PieceMovesRequestSerializer,
        responses=PieceMovesResponseSerializer,
        examples=[
            OpenApiExample(
                'Example 1',
                description='Example with a knight in the h1 position on a '
                '4x4 board.',
                value={
                    'first': ['f2', 'g3'],
                    'second': {
                        'f2': ['h3', 'g4', 'e4', 'd3', 'd1'],
                        'g3': ['h5', 'f5', 'e4', 'e2', 'f1'],
                    },
                },
            ),
        ],
    )
    @action(detail=True, methods=['get'], name='Next moves of the piece')
    def moves(self, request, pk: int = None):
        """
        Returns the next possible moves of the piece from the informed origin.
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
