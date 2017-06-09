from __future__ import unicode_literals

import requests
from box import Box


class Client:
    RUN_QUERY = '/run-query'

    def __init__(self, url, extra_params=None):
        self.url = url
        self.params = extra_params or {}

    def run_query(self, query, params=None):
        params = dict(list(self.params.items()) + list(params.items())) if params else self.params
        response = requests.post(self.url + self.RUN_QUERY, params=params, data=query,
                                 headers={'Content-type': 'text/plain'})

        return Response(response)

    def run_named_query(self, namespace, name, revision, params=None):
        params = dict(list(self.params.items()) + list(params.items())) if params else self.params
        url = self.url + self.RUN_QUERY + '/{namespace}/{name}/{revision}'.format(namespace=namespace, name=name,
                                                                                  revision=revision)
        response = requests.get(url, params=params, headers={'Content-type': 'text/plain'})

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
