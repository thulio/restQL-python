from __future__ import unicode_literals

import requests
import six
from box import Box


class Client:
    RUN_QUERY = '/run-query'
    PARSE_QUERY = '/parse-query'

    def __init__(self, url, extra_params=None):
        self.url = url
        self.params = extra_params or {}
        self.headers = {'Content-type': 'text/plain'}

    def run_query(self, query, params=None):
        params = self._build_params(params)
        response = requests.post(self.url + self.RUN_QUERY, params=params, data=query,
                                 headers=self.headers)

        return Response(response)

    def run_named_query(self, namespace, name, revision, params=None):
        params = self._build_params(params)
        url = self.url + self.RUN_QUERY + '/{namespace}/{name}/{revision}'.format(namespace=namespace, name=name,
                                                                                  revision=revision)
        response = requests.get(url, params=params, headers=self.headers)

        return Response(response)

    def parse_query(self, query):
        response = requests.post(self.url + self.PARSE_QUERY, data=query, headers=self.headers)

        return response.ok

    def _build_params(self, params):
        if params:
            new_params = self.params.copy()
            new_params.update(params)
        else:
            new_params = self.params

        return new_params


class Response(object):
    def __init__(self, http_response):
        self.response = http_response
        self.status, self.resources = self._get_resources()

    def _get_resources(self):
        json_data = self.response.json()
        resources_names = six.iterkeys(json_data)
        resources = {}
        status = {}
        for resource in resources_names:
            data = json_data[resource]
            if isinstance(data, dict):
                status[resource] = Box(data['details'])
                resources[resource] = Box(data['result'])

            elif isinstance(data, list):
                resources[resource] = [Box(d['result']) for d in data]
                status[resource] = [Box(d['details']) for d in data]

        return status, resources

    def ok(self):
        for key, value in six.iteritems(self.status):
            if isinstance(value, list):
                for status in value:
                    if not status.success:
                        return False
            else:
                if not value.success:
                    return False

        return True

    def __getattr__(self, item):
        return self.resources[item]


if __name__ == '__main__':  # pragma: no cover
    client = Client('http://localhost:9000')
    response = client.run_query("from planets as allPlanets")
    print(response.allPlanets)
