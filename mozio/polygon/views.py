from django.contrib.gis.geos import GEOSGeometry
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


from .models import Polygon
from .serializers import PolygonSerializer, PointsSerializer


class PolygonViewSet(viewsets.ModelViewSet):
    """Api to allow viewing and editing of Polygons"""
    queryset = Polygon.objects.all()
    serializer_class = PolygonSerializer

    @action(detail=False)
    def get_locations(self, request):
        long = request.query_params.get('long')
        lat = request.query_params.get('lat')
        points_serializer = PointsSerializer(
            data={"lat": lat, "long": long})
        points_serializer.is_valid(raise_exception=True)
        poly_object_data = f'POINT ({long} {lat})'
        geom = GEOSGeometry(poly_object_data)
        polys = Polygon.objects.filter(poly__bbcontains=geom)
        serializer = self.get_serializer(polys, many=True)

        return Response(serializer.data)
