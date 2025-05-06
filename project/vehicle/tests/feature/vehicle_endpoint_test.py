from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from project.vehicle.models import Vehicle
from project.vehicle.tests.factories import VehicleFactory


class ListAndRetrieveVehicleEndpointTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        User.objects.create_user("albert", "albert@einstein.com", "relativity")
        VehicleFactory.create_batch(34)

    def setUp(self):
        user = User.objects.get(email="albert@einstein.com")
        refresh = RefreshToken.for_user(user)
        jwt = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt}")

    def test_listing_options(self):
        response = self.client.options("/vehicles/")
        headers = response.headers
        self.assertIn("GET", headers.get("Allow"))
        self.assertIn("POST", headers.get("Allow"))
        self.assertNotIn("PUT", headers.get("Allow"))
        self.assertNotIn("PATCH", headers.get("Allow"))
        self.assertNotIn("DELETE", headers.get("Allow"))

    def test_listing(self):
        response = self.client.get("/vehicles/", HTTP_ACCEPT="application/json; version=1")

        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())
        self.assertIn("pagination", response.json()["meta"])
        self.assertIn("meta", response.json())

        data = response.json()["data"]
        meta = response.json()["meta"]
        pagination = meta["pagination"]

        self.assertEqual(len(data), 10)
        self.assertEqual(pagination["total"], 34)
        self.assertEqual(pagination["current_page"], 1)
        self.assertEqual(pagination["total_pages"], 4)
        self.assertEqual(pagination["page_size"], 10)
        self.assertEqual(pagination["count"], 10)

        self.assertIn("timestamp", meta)

    def test_listing_page_2(self):
        response = self.client.get("/vehicles/?page=2")

        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())
        self.assertIn("pagination", response.json()["meta"])
        self.assertIn("meta", response.json())

        data = response.json()["data"]
        meta = response.json()["meta"]
        pagination = meta["pagination"]

        self.assertEqual(len(data), 10)
        self.assertEqual(pagination["total"], 34)
        self.assertEqual(pagination["current_page"], 2)
        self.assertEqual(pagination["total_pages"], 4)
        self.assertEqual(pagination["page_size"], 10)
        self.assertEqual(pagination["count"], 10)

        self.assertIn("timestamp", meta)

    def test_listing_page_4(self):
        response = self.client.get("/vehicles/?page=4")

        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())
        self.assertIn("pagination", response.json()["meta"])
        self.assertIn("meta", response.json())

        data = response.json()["data"]
        meta = response.json()["meta"]
        pagination = meta["pagination"]

        self.assertEqual(len(data), 4)
        self.assertEqual(pagination["total"], 34)
        self.assertEqual(pagination["current_page"], 4)
        self.assertEqual(pagination["total_pages"], 4)
        self.assertEqual(pagination["page_size"], 10)
        self.assertEqual(pagination["count"], 4)

        self.assertIn("timestamp", meta)

    def test_listing_page_over(self):

        # Here we test page 9, which is not exist.
        response = self.client.get("/vehicles/?page=9")

        self.assertEqual(response.status_code, 404)
        self.assertNotIn("data", response.json())
        self.assertIn("error", response.json())
        self.assertIn("meta", response.json())

        error = response.json()["error"]
        meta = response.json()["meta"]

        self.assertEqual(error["code"], 404)
        self.assertEqual(error["message"], "Nothing matches the given URI")
        self.assertEqual(error["detail"], "Invalid page.")

        self.assertIn("timestamp", meta)

    def test_retrieve(self):
        vehicle = Vehicle.objects.order_by("?").last()
        response = self.client.get(f"/vehicles/{vehicle.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())
        self.assertNotIn("pagination", response.json()["meta"])
        self.assertIn("meta", response.json())

        data = response.json()["data"]
        meta = response.json()["meta"]

        self.assertEqual(vehicle.id, data["id"])
        self.assertIn("_link_", data)

        self.assertIn("timestamp", meta)


class CreateVehicleEndpointTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Prepare user and password
        User.objects.create_user("albert", "albert@einstein.com", "relativity")

    def setUp(self):

        user = User.objects.get(email="albert@einstein.com")
        refresh = RefreshToken.for_user(user)
        self.jwt = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.jwt}")

    def test_authenticated(self):
        response = self.client.post(
            "/vehicles/",
            data={"wheel": 12},
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("data", response.json())
        self.assertNotIn("pagination", response.json()["meta"])
        self.assertIn("meta", response.json())

        data = response.json()["data"]
        meta = response.json()["meta"]

        self.assertEqual(12, data["wheel"])
        self.assertIn("_link_", data)

        self.assertIn("timestamp", meta)

    def test_unauthenticated(self):
        self.client.credentials()  # Remove any credential
        response = self.client.post("/vehicles/", data={"wheel": 12})

        self.assertEqual(response.status_code, 401)
        self.assertNotIn("data", response.json())
        self.assertIn("error", response.json())
        self.assertNotIn("pagination", response.json()["meta"])
        self.assertIn("meta", response.json())

        error = response.json()["error"]
        meta = response.json()["meta"]

        self.assertEqual("No permission -- see authorization schemes", error["message"])
        self.assertEqual("Need valid authentication mechanism", error["detail"])

        self.assertIn("timestamp", meta)

    def test_wrong_token_key(self):
        self.client.credentials()  # Remove any credential
        response = self.client.post(
            "/vehicles/",
            data={"wheel": 12},
            # Force credential here, change it to Token to mimic wrong request.
            HTTP_AUTHORIZATION=f"Token {self.jwt}",
        )

        self.assertEqual(response.status_code, 401)
        self.assertNotIn("data", response.json())
        self.assertIn("error", response.json())
        self.assertNotIn("pagination", response.json()["meta"])
        self.assertIn("meta", response.json())

        error = response.json()["error"]
        meta = response.json()["meta"]

        self.assertEqual("No permission -- see authorization schemes", error["message"])
        self.assertEqual("Need valid authentication mechanism", error["detail"])

        self.assertIn("timestamp", meta)


class UpdateVehicleEndpointTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Prepare user and password
        User.objects.create_user("albert", "albert@einstein.com", "relativity")

    def setUp(self):
        user = User.objects.get(email="albert@einstein.com")
        refresh = RefreshToken.for_user(user)
        self.jwt = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.jwt}")
        self.vehicle = VehicleFactory()

    def test_authenticated(self):
        response = self.client.put(
            f"/vehicles/{self.vehicle.id}/",
            data={"wheel": 12},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())
        self.assertNotIn("pagination", response.json()["meta"])
        self.assertIn("meta", response.json())

        data = response.json()["data"]
        meta = response.json()["meta"]

        self.assertEqual(12, data["wheel"])
        self.assertIn("_link_", data)

        self.assertIn("timestamp", meta)

    def test_unauthenticated(self):
        self.client.credentials()
        response = self.client.put(f"/vehicles/{self.vehicle.id}/", data={"wheel": 12})

        self.assertEqual(response.status_code, 401)
        self.assertNotIn("data", response.json())
        self.assertIn("error", response.json())
        self.assertNotIn("pagination", response.json()["meta"])
        self.assertIn("meta", response.json())

        error = response.json()["error"]
        meta = response.json()["meta"]

        self.assertEqual("No permission -- see authorization schemes", error["message"])
        self.assertEqual("Need valid authentication mechanism", error["detail"])

        self.assertIn("timestamp", meta)

    def test_wrong_token_key(self):
        self.client.credentials()
        response = self.client.put(
            f"/vehicles/{self.vehicle.id}/",
            data={"wheel": 12},
            HTTP_AUTHORIZATION=f"Token {self.jwt}",  # <- Should be Bearer
        )

        self.assertEqual(response.status_code, 401)
        self.assertNotIn("data", response.json())
        self.assertIn("error", response.json())
        self.assertNotIn("pagination", response.json()["meta"])
        self.assertIn("meta", response.json())

        error = response.json()["error"]
        meta = response.json()["meta"]

        self.assertEqual("No permission -- see authorization schemes", error["message"])
        self.assertEqual("Need valid authentication mechanism", error["detail"])

        self.assertIn("timestamp", meta)


class DeleteVehicleEndpointTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Prepare user and password
        User.objects.create_user("albert", "albert@einstein.com", "relativity")

    def setUp(self):
        user = User.objects.get(email="albert@einstein.com")
        refresh = RefreshToken.for_user(user)
        self.jwt = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.jwt}")
        self.vehicle = VehicleFactory()

    def test_authenticated(self):
        response = self.client.delete(
            f"/vehicles/{self.vehicle.id}/",
            data={"wheel": 12},
        )

        self.assertEqual(response.status_code, 204)
        self.assertIsNone(response.data)

    def test_unauthenticated(self):
        self.client.credentials()
        response = self.client.delete(f"/vehicles/{self.vehicle.id}/", data={"wheel": 12})
        self.assertEqual(response.status_code, 401)
        self.assertNotIn("data", response.json())
        self.assertIn("error", response.json())
        self.assertNotIn("pagination", response.json()["meta"])
        self.assertIn("meta", response.json())

        error = response.json()["error"]
        meta = response.json()["meta"]

        self.assertEqual("No permission -- see authorization schemes", error["message"])
        self.assertEqual("Need valid authentication mechanism", error["detail"])

        self.assertIn("timestamp", meta)

    def test_wrong_token_key(self):
        self.client.credentials()
        response = self.client.delete(
            f"/vehicles/{self.vehicle.id}/",
            data={"wheel": 12},
            HTTP_AUTHORIZATION=f"Token {self.jwt}",  # <- Should be Bearer
        )

        self.assertEqual(response.status_code, 401)
        self.assertNotIn("data", response.json())
        self.assertIn("error", response.json())
        self.assertNotIn("pagination", response.json()["meta"])
        self.assertIn("meta", response.json())

        error = response.json()["error"]
        meta = response.json()["meta"]

        self.assertEqual("No permission -- see authorization schemes", error["message"])
        self.assertEqual("Need valid authentication mechanism", error["detail"])

        self.assertIn("timestamp", meta)
