from __future__ import unicode_literals

import requests
from box import Box


class Client:
    RUN_QUERY = '/run-query'

    def __init__(self, url, extra_params=None):
        self.url = url
        self.params = extra_params

    def run_query(self, query):
        response = requests.post(self.url + self.RUN_QUERY, params=self.params, data=query,
                                 headers={'Content-type': 'text/plain'})

        return Response(response)


class Response(object):
    def __init__(self, http_response):
        self.response = http_response
        self.resources = self._get_resources()

    def _get_resources(self):
        json_data = self.response.json()
        resources_names = list(json_data.keys())
        resources = {}
        for resource in resources_names:
            data = json_data[resource]
            if isinstance(data, dict):
                resources[resource] = Box(data['result'])

            elif isinstance(data, list):
                resources[resource] = [Box(d['result']) for d in data]

        return resources

    def __getattr__(self, item):
        return self.resources[item]


if __name__ == '__main__':  # pragma: no cover
    client = Client('http://localhost:9000')
    response = client.run_query("from planets as allPlanets")
    print(response.allPlanets)
