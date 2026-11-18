"""Regresión del contrato HTTP existente; no requiere servidor ni PostgreSQL."""

import unittest

from fastapi.testclient import TestClient

from backend.app.main import app


class ApiContractTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def tearDown(self):
        self.client.close()

    def test_root_and_openapi(self):
        self.assertEqual(self.client.get("/").status_code, 200)
        paths = self.client.get("/openapi.json").json()["paths"]
        self.assertIn("/api/destinations", paths)
        self.assertIn("/api/recommendations", paths)

    def test_catalog_contract(self):
        response = self.client.get("/api/destinations")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total"], len(data["destinations"]))
        self.assertGreater(data["total"], 0)
        required = {"id", "name", "municipality", "category", "price", "days", "tags"}
        for destination in data["destinations"]:
            self.assertTrue(required.issubset(destination))

    def test_recommendation_contract_and_catalog_unchanged(self):
        before = self.client.get("/api/destinations").json()
        response = self.client.post("/api/recommendations", json={
            "days": 2, "budget": 200000, "interests": ["naturaleza"]
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertLessEqual(len(data["itinerary"]), 2)
        self.assertGreater(len(data["itinerary"]), 0)
        self.assertEqual(data["estimated_total"], sum(d["price"] for d in data["itinerary"]))
        self.assertEqual(data["remaining_budget"], max(200000 - data["estimated_total"], 0))
        self.assertEqual(before, self.client.get("/api/destinations").json())

    def test_unknown_or_empty_interests_keep_existing_fallback(self):
        for interests in ([], ["sin-coincidencias"]):
            with self.subTest(interests=interests):
                response = self.client.post("/api/recommendations", json={
                    "days": 1, "budget": 200000, "interests": interests
                })
                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(response.json()["itinerary"]), 1)

    def test_zero_budget_documents_existing_first_stop_exception(self):
        response = self.client.post("/api/recommendations", json={
            "days": 1, "budget": 0, "interests": []
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Comportamiento actual: permite una parada aunque exceda presupuesto.
        self.assertEqual(len(data["itinerary"]), 1)
        self.assertGreater(data["estimated_total"], 0)
        self.assertEqual(data["remaining_budget"], 0)

    def test_request_boundaries(self):
        for days in (1, 14):
            response = self.client.post("/api/recommendations", json={
                "days": days, "budget": 100000000, "interests": []
            })
            self.assertEqual(response.status_code, 200)
            self.assertLessEqual(len(response.json()["itinerary"]), days)

    def test_invalid_requests_return_422(self):
        for payload in ({"days": 0}, {"days": 15}, {"budget": -1},
                        {"budget": 100000001}, {"days": "invalid"},
                        {"interests": "naturaleza"}):
            with self.subTest(payload=payload):
                self.assertEqual(self.client.post("/api/recommendations", json=payload).status_code, 422)

    def test_cors_allows_local_frontend_only(self):
        for origin, allowed in (("http://localhost:5173", True),
                                ("https://untrusted.example", False)):
            response = self.client.get("/api/destinations", headers={"Origin": origin})
            self.assertEqual("access-control-allow-origin" in response.headers, allowed)


if __name__ == "__main__":
    unittest.main()
