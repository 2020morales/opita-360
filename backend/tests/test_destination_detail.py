"""S01 AC-01..03: detail contract, validation and unchanged catalogue."""
import unittest
from fastapi.testclient import TestClient
from backend.app.main import app

class DestinationDetailTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.before = self.client.get("/api/destinations").json()

    def tearDown(self):
        self.assertEqual(self.client.get("/api/destinations").json(), self.before)
        self.client.close()

    def test_existing_destination_matches_every_catalogue_field(self):
        for destination in self.before["destinations"]:
            with self.subTest(id=destination["id"]):
                response = self.client.get(f"/api/destinations/{destination['id']}")
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json(), {"destination": destination})

    def test_missing_destination_has_no_fallback(self):
        response = self.client.get("/api/destinations/9999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Destino no encontrado"})

    def test_invalid_ids_are_rejected(self):
        for value in ("abc", "0", "-1", "1.5"):
            with self.subTest(value=value):
                self.assertEqual(self.client.get(f"/api/destinations/{value}").status_code, 422)

    def test_detail_route_is_documented(self):
        schema = self.client.get("/openapi.json").json()
        self.assertIn("/api/destinations/{destination_id}", schema["paths"])

if __name__ == "__main__":
    unittest.main()
