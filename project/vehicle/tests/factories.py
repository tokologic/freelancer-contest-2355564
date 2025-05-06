from factory import django

from project.vehicle.models import Vehicle


class VehicleFactory(django.DjangoModelFactory):
    class Meta:
        model = Vehicle

    wheel = 4
