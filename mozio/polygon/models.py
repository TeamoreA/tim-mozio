from django.contrib.gis.db import models
from mozio.provider.models import Provider


class Polygon(models.Model):
    """
    Creates a model to hold a polygon object instance
    """
    name = models.CharField(max_length=255)
    provider = models.ForeignKey(
        Provider, on_delete=models.PROTECT, related_name='polygons')
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    poly = models.PolygonField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """
        Return a string representation of Polygon object
        """
        return self.name

    class Meta:
        unique_together = (('name', 'provider'), )
        ordering = ('-created',)
