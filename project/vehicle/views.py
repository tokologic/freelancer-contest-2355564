from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from project.vehicle.models import Vehicle
from project.vehicle.serializers import VehicleSerializer


class VehicleViewSet(viewsets.ModelViewSet):

    queryset = Vehicle.objects.order_by("id")
    serializer_class = VehicleSerializer

    @extend_schema(summary="List all vehicles")
    def list(self, request, *args, **kwargs):
        """The list all vehicles endpoint retrieves a paginated list of all vehicles stored in the system.
        Each vehicle entry includes key attributes such as its unique identifier and number of wheels.
        This endpoint supports query parameters for pagination, allowing clients to efficiently
        navigate large datasets."""

        return super().list(request, *args, **kwargs)

    @extend_schema(summary="Create vehicle")
    def create(self, request, *args, **kwargs):
        """The create vehicle endpoint allows clients to add a new vehicle record to the system
        by submitting the required vehicle data in the request body.
        This includes attributes such as the number of wheels and any other relevant vehicle details.
        Upon successful validation and creation, the endpoint returns the newly created vehicle
        along with a unique identifier."""

        return super().create(request, *args, **kwargs)

    @extend_schema(summary="Get vehicle detail")
    def retrieve(self, request, *args, **kwargs):
        """The Retrieve Vehicle endpoint fetches detailed information about a specific vehicle
        identified by its unique ID. This endpoint is useful when a client needs to view
        the full details of a single vehicle, such as in a detail page or editing form.
        If the vehicle exists, the system returns its data; otherwise,
        a 404 Not Found response is returned. This endpoint ensures accurate
        and secure access to individual vehicle records."""

        return super().retrieve(request, *args, **kwargs)

    @extend_schema(summary="Update vehicle")
    def update(self, request, *args, **kwargs):
        """The update vehicle endpoint allows clients to modify the details of an existing vehicle
        by specifying its unique ID and providing the updated data in the request body.
        This endpoint supports full updates (via PUT) or partial updates (via PATCH),
        enabling flexibility in how changes are applied.
        Upon successful validation, the system updates the vehicle record and returns the updated data.
        If the vehicle is not found, a 404 Not Found response is returned."""

        return super().update(request, *args, **kwargs)

    @extend_schema(summary="Patch vehicle")
    def partial_update(self, request, *args, **kwargs):
        """The update vehicle endpoint allows clients to modify the details of an existing vehicle
        by specifying its unique ID and providing the updated data in the request body.
        This endpoint supports full updates (via PUT) or partial updates (via PATCH),
        enabling flexibility in how changes are applied.
        Upon successful validation, the system updates the vehicle record and returns the updated data.
        If the vehicle is not found, a 404 Not Found response is returned."""

        return super().partial_update(request, *args, **kwargs)

    @extend_schema(summary="Delete vehicle")
    def destroy(self, request, *args, **kwargs):
        """The delete vehicle endpoint allows clients to remove a specific vehicle from the system
        using its unique ID. Once the vehicle is successfully deleted, the endpoint returns
        a 204 No Content response to indicate the operation was completed without returning any data.
        If the specified vehicle does not exist, a 404 Not Found response is returned."""

        return super().destroy(request, *args, **kwargs)
