import unittest

import mock
import requests

from restQL.client import Client
from tests import load_fixture


class TestClient(unittest.TestCase):
    def setUp(self):
        self.requests_post_patcher = mock.patch.object(requests, 'post')
        self.requests_post_mock = self.requests_post_patcher.start()

        self.requests_get_patcher = mock.patch.object(requests, 'get')
        self.requests_get_mock = self.requests_get_patcher.start()

    def tearDown(self):
        self.requests_post_patcher.stop()
        self.requests_get_patcher.stop()

    def test_simple_query(self):
        query = "from planets as allPlanets"
        response_mock = mock.Mock()
        response_mock.status_code = 200
        response_mock.json.return_value = load_fixture('allPlanets.json')
        self.requests_post_mock.return_value = response_mock

        client = Client('http://localhost:9000')
        response = client.run_query(query)

        self.assertEqual(self.requests_post_mock.call_count, 1)
        self.assertEqual(self.requests_post_mock.call_args_list, [mock.call('http://localhost:9000/run-query',
                                                                            data='from planets as allPlanets',
                                                                            headers={'Content-type': 'text/plain'},
                                                                            params={})])
        self.assertEqual(response.allPlanets.count, 2)
        self.assertEqual(len(response.allPlanets.results), 2)

    def test_simple_named_query(self):
        response_mock = mock.Mock()
        response_mock.status_code = 200
        response_mock.json.return_value = load_fixture('allPlanets.json')
        self.requests_get_mock.return_value = response_mock

        client = Client('http://localhost:9000')
        response = client.run_named_query('ns', 'query', 1)

        self.assertEqual(self.requests_get_mock.call_count, 1)
        self.assertEqual(self.requests_get_mock.call_args_list, [mock.call('http://localhost:9000/run-query/ns/query/1',
                                                                           headers={'Content-type': 'text/plain'},
                                                                           params={})])
        self.assertEqual(response.allPlanets.count, 2)
        self.assertEqual(len(response.allPlanets.results), 2)

    def test_nested_result(self):
        query = "from planets as allPlanets"
        response_mock = mock.Mock()
        response_mock.status_code = 200
        response_mock.json.return_value = load_fixture('nestedPlanets.json')
        self.requests_post_mock.return_value = response_mock

        client = Client('http://localhost:9000')
        response = client.run_query(query)

        self.assertEqual(self.requests_post_mock.call_count, 1)
        self.assertEqual(self.requests_post_mock.call_args_list, [mock.call('http://localhost:9000/run-query',
                                                                            data='from planets as allPlanets',
                                                                            headers={'Content-type': 'text/plain'},
                                                                            params={})])
        self.assertTrue(isinstance(response.allPlanets, list))
        self.assertEqual(len(response.allPlanets[0].results), 2)
