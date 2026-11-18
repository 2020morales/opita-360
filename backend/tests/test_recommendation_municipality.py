"""S04: real HTTP contracts via TestClient; no deployed-server claims."""
import unittest
from fastapi.testclient import TestClient
from backend.app.main import app

class MunicipalityRecommendationTests(unittest.TestCase):
    def setUp(self):
        self.client=TestClient(app)
        self.catalog=self.client.get('/api/destinations').json()
    def tearDown(self):
        self.assertEqual(self.client.get('/api/destinations').json(),self.catalog)
        self.client.close()
    def post(self,**values):
        return self.client.post('/api/recommendations',json={'days':2,'budget':200000,'interests':['naturaleza'],**values})
    def test_legacy_contract_fixture(self):
        r=self.post();self.assertEqual(r.status_code,200);d=r.json()
        self.assertEqual([x['id'] for x in d['itinerary']],[6,5]);self.assertEqual(d['estimated_total'],135000);self.assertEqual(d['remaining_budget'],65000)
        self.assertEqual(set(d),{'summary','method','itinerary','estimated_total','budget','remaining_budget','notice'})
    def test_omitted_null_and_empty_are_equivalent(self):
        expected=self.post().json()
        for value in (None,'','   '):
            with self.subTest(value=value):self.assertEqual(self.post(municipality=value).json(),expected)
    def test_neiva_recovery_never_escapes_municipality(self):
        for interests in (['naturaleza'],[],['sin-coincidencias'],['cultura']):
            with self.subTest(interests=interests):
                d=self.post(municipality='Neiva',interests=interests,days=14,budget=100000000).json()
                self.assertEqual({x['id'] for x in d['itinerary']},{3,8});self.assertTrue(all(x['municipality']=='Neiva' for x in d['itinerary']))
    def test_case_spaces_and_accents(self):
        a=self.post(municipality='San Agustín').json();b=self.post(municipality='  sAn aGuStÍn  ').json()
        self.assertEqual(a,b);self.assertTrue(a['itinerary']);self.assertTrue(all(x['municipality']=='San Agustín' for x in a['itinerary']))
    def test_unknown_municipality_is_empty_with_full_budget(self):
        d=self.post(municipality='Municipio sin destinos',budget=123456).json()
        self.assertEqual(d['itinerary'],[]);self.assertEqual(d['estimated_total'],0);self.assertEqual(d['budget'],123456);self.assertEqual(d['remaining_budget'],123456)
        self.assertIn('No hay destinos',d['notice'])
    def test_nonstring_municipality_is_rejected(self):
        for value in (123,True,[],{}):
            with self.subTest(value=value):self.assertEqual(self.post(municipality=value).status_code,422)
    def test_existing_first_stop_budget_exception_is_preserved(self):
        d=self.post(municipality='Neiva',budget=0,days=1).json()
        self.assertEqual([x['id'] for x in d['itinerary']],[3]);self.assertEqual(d['estimated_total'],35000);self.assertEqual(d['remaining_budget'],0)
    def test_optional_field_is_in_openapi(self):
        schema=self.client.get('/openapi.json').json()['components']['schemas']['TripRequest']
        self.assertIn('municipality',schema['properties']);self.assertNotIn('municipality',schema.get('required',[]))
