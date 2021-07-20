from rest_framework import viewsets

from .models import Provider
from .serializers import ProviderSerializer


class ProviderViewSet(viewsets.ModelViewSet):
    """Api to allow viewing and editing of providers"""
    queryset = Provider.objects.all().order_by('-created')
    serializer_class = ProviderSerializer
