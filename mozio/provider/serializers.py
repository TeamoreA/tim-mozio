from rest_framework import serializers

from .models import Provider


class ProviderSerializer(serializers.ModelSerializer):
    """
    serializer provider data and support some serializer validations
    """
    class Meta:
        model = Provider
        fields = "__all__"
