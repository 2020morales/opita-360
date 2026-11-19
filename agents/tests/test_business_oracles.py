"""Oráculos fijos del catálogo de demostración; no cambian reglas turísticas."""
import unittest
from fastapi.testclient import TestClient
from backend.app.main import app


class BusinessOracleTests(unittest.TestCase):
    def test_nature_two_days_fixed_expected_itinerary(self):
        with TestClient(app) as client:
            response = client.post("/api/recommendations", json={"days": 2, "budget": 200000, "interests": ["naturaleza"]})
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual([d["id"] for d in result["itinerary"]], [6, 5])
        self.assertEqual(result["estimated_total"], 135000)
        self.assertEqual(result["remaining_budget"], 65000)

    def test_budget_boundary_excludes_second_destination(self):
        with TestClient(app) as client:
            result = client.post("/api/recommendations", json={"days": 2, "budget": 134999, "interests": ["naturaleza"]}).json()
        self.assertEqual([d["id"] for d in result["itinerary"]], [6])
        self.assertEqual(result["estimated_total"], 65000)
        self.assertEqual(result["remaining_budget"], 69999)
