"""Regresiones de la revisión: catálogo sincronizado, avisos y límites de entrada."""
import json
from pathlib import Path
import unittest

from fastapi.testclient import TestClient

from backend.app.main import DESTINATIONS, app

FALLBACK = Path(__file__).resolve().parents[2] / "frontend/src/fallback-destinations.json"


class ReviewFixesTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def tearDown(self):
        self.client.close()

    def post(self, **payload):
        return self.client.post("/api/recommendations", json=payload)

    def test_rev07_frontend_fallback_catalog_matches_api(self):
        self.assertEqual(json.loads(FALLBACK.read_text(encoding="utf-8")), DESTINATIONS)

    def test_rev03_zero_budget_keeps_first_stop_but_warns(self):
        data = self.post(days=1, budget=0, interests=["naturaleza"]).json()
        self.assertEqual(len(data["itinerary"]), 1)
        self.assertIn("supera tu presupuesto", data["notice"])

    def test_rev03_no_budget_warning_when_within_budget(self):
        data = self.post(days=1, budget=200000, interests=["naturaleza"]).json()
        self.assertNotIn("supera tu presupuesto", data["notice"])

    def test_rev04_interest_list_and_item_size_are_bounded(self):
        self.assertEqual(self.post(interests=["naturaleza"] * 21).status_code, 422)
        self.assertEqual(self.post(interests=["x" * 41]).status_code, 422)
        self.assertEqual(self.post(municipality="x" * 101).status_code, 422)
        self.assertEqual(self.post(interests=["naturaleza"] * 20).status_code, 200)

    def test_rev05_interests_ignore_case_and_outer_spaces(self):
        data = self.post(days=2, budget=200000, interests=["  Naturaleza "]).json()
        self.assertEqual([d["id"] for d in data["itinerary"]], [6, 5])

    def test_rev06_fewer_stops_than_days_is_announced(self):
        data = self.post(days=14, budget=100000000, interests=["naturaleza"]).json()
        self.assertLess(len(data["itinerary"]), 14)
        self.assertIn(f"{len(data['itinerary'])} parada(s) para 14 día(s)", data["notice"])


if __name__ == "__main__":
    unittest.main()
