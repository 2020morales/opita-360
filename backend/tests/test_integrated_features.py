"""Joint S01/S04 contracts using the real FastAPI app in-process."""
import unittest
from fastapi.testclient import TestClient
from backend.app.main import app

class IntegratedFeatureTests(unittest.TestCase):
    def test_recommended_destinations_have_matching_detail(self):
        with TestClient(app) as client:
            before = client.get('/api/destinations').json()
            response = client.post('/api/recommendations', json={'days': 2, 'budget': 200000, 'interests': ['naturaleza'], 'municipality': 'Neiva'})
            self.assertEqual(response.status_code, 200)
            proposal = response.json()
            self.assertEqual({d['id'] for d in proposal['itinerary']}, {3, 8})
            for item in proposal['itinerary']:
                detail = client.get('/api/destinations/' + str(item['id']))
                self.assertEqual(detail.status_code, 200)
                self.assertEqual(detail.json()['destination'], item)
            self.assertEqual(client.get('/api/destinations').json(), before)

    def test_empty_recommendation_does_not_change_detail_or_legacy_budget(self):
        with TestClient(app) as client:
            empty = client.post('/api/recommendations', json={'municipality': 'Sin destinos', 'budget': 123456}).json()
            self.assertEqual(empty['itinerary'], [])
            self.assertEqual(empty['remaining_budget'], 123456)
            self.assertEqual(client.get('/api/destinations/9999').status_code, 404)
            zero = client.post('/api/recommendations', json={'municipality': 'Neiva', 'budget': 0}).json()
            self.assertEqual(zero['itinerary'][0]['id'], 3)
            self.assertEqual(zero['estimated_total'], 35000)
            self.assertEqual(zero['remaining_budget'], 0)
