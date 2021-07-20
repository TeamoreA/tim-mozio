from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos.error import GEOSException
from rest_framework import serializers

from .models import Polygon
from mozio.provider.models import Provider


class PointsSerializer(serializers.Serializer):
    """
    Serialize latitude and logitude input query params
    """
    long = serializers.CharField()
    lat = serializers.CharField()

    def validate(self, data):
        lat = data['lat']
        long = data['long']
        try:
            float(long)
            float(lat)
        except ValueError:
            raise serializers.ValidationError(
                {'geo_points': 'Ensure the points are numbers'})
        return data


class PolygonSerializer(serializers.ModelSerializer):
    """
    serializer polygon data and support some serializer validations
    """
    provider_name = serializers.SerializerMethodField()

    class Meta:
        model = Polygon
        fields = "__all__"
        fields = ["id", "name", "provider_name", "price", "created", "updated"]

    def get_provider_name(self, obj):
        return obj.provider.name

    def validate(self, data):
        """
        Validate that the suplied provider id is valid and the user exists

        validate that entered polygon points are valid

        i.e Forms a valid polygon with more than three points
        Entered values are digits
        """
        provider_id = self.initial_data['provider']
        try:
            provider = Provider.objects.get(id=provider_id)
            data['provider'] = provider
        except Provider.DoesNotExist:
            raise serializers.ValidationError(
                    {'provider': 'Please enter a valid provider'})

        poly_points = self.initial_data['poly']
        for poly_point in poly_points:
            if len(poly_points) < 3:
                raise serializers.ValidationError(
                    {'poly': 'Please enter more than three pair of points'})
            elif len(poly_point.split()) != 2:
                raise serializers.ValidationError(
                    {'poly': 'Please a pair of valid points for latitude and longitude'})
            for val in poly_point.split():
                try:
                    float(val)
                except ValueError:
                    raise serializers.ValidationError(
                        {'poly': 'Ensure the points are numbers'})
        poly_data = ", ".join(poly_points)
        poly_object_data = f'POLYGON (({poly_data}))'

        try:
            data['poly'] = GEOSGeometry(poly_object_data)
        except GEOSException:
            raise serializers.ValidationError(
                {'poly': 'Points of LinearRing do not form a closed linestring.'})

        return data
