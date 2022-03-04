from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Piece
from core.serializers import PieceSerializer


def hello_world(request):
    return JsonResponse({'hello': 'world'})


class PieceViewSet(viewsets.ModelViewSet):
    queryset = Piece.objects.all().order_by('color')
    serializer_class = PieceSerializer

    @action(detail=True, methods=['get'])
    def movements(self, request, pk=None):
        piece = Piece.objects.get(pk=pk)

        origin = request.query_params.get('origin')
        if origin is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        movements = []

        if piece.type is Piece.Type.KNIGHT.value:
            movements.append('b6')

        return Response({'movements': movements})
