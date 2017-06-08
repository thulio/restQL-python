import unittest

import mock
import requests

from restQL.client import Client


class TestClient(unittest.TestCase):
    def setUp(self):
        self.requests_patcher = mock.patch.object(requests, 'post')
        self.requests_mock = self.requests_patcher.start()

    def tearDown(self):
        self.requests_patcher.stop()

    def test_simple_query(self):
        query = "from planets as allPlanets"
        response_mock = mock.Mock()
        response_mock.status_code = 200
        response_mock.json.return_value = {
            "allPlanets": {
                "details": {
                    "success": True,
                    "status": 200,
                    "metadata": {}
                },
                "result": {
                    "count": 2,
                    "next": "http://swapi.co/api/planets/?page=2",
                    "previous": None,
                    "results": [
                        {
                            "surface_water": "40",
                            "climate": "temperate",
                            "residents": [
                                "http://swapi.co/api/people/5/",
                                "http://swapi.co/api/people/68/",
                                "http://swapi.co/api/people/81/"
                            ],
                            "orbital_period": "364",
                            "name": "Alderaan",
                            "diameter": "12500",
                            "created": "2014-12-10T11:35:48.479000Z",
                            "gravity": "1 standard",
                            "edited": "2014-12-20T20:58:18.420000Z",
                            "films": [
                                "http://swapi.co/api/films/6/",
                                "http://swapi.co/api/films/1/"
                            ],
                            "population": "2000000000",
                            "terrain": "grasslands, mountains",
                            "url": "http://swapi.co/api/planets/2/",
                            "rotation_period": "24"
                        },
                        {
                            "surface_water": "8",
                            "climate": "temperate, tropical",
                            "residents": [],
                            "orbital_period": "4818",
                            "name": "Yavin IV",
                            "diameter": "10200",
                            "created": "2014-12-10T11:37:19.144000Z",
                            "gravity": "1 standard",
                            "edited": "2014-12-20T20:58:18.421000Z",
                            "films": [
                                "http://swapi.co/api/films/1/"
                            ],
                            "population": "1000",
                            "terrain": "jungle, rainforests",
                            "url": "http://swapi.co/api/planets/3/",
                            "rotation_period": "24"
                        }]}}}
        self.requests_mock.return_value = response_mock

        client = Client('http://localhost:9000')
        response = client.run_query(query)

        self.assertEqual(response.allPlanets.count, 2)
        self.assertEqual(len(response.allPlanets.results), 2)
