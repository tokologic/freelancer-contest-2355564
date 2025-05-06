from rest_framework import serializers

from project.restful.mixins import HATEOASMixin
from project.vehicle.models import Vehicle


class VehicleSerializer(HATEOASMixin, serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ["id", "wheel"]
