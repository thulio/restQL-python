import json
import os.path
import sys

HERE = os.path.abspath(os.path.dirname(__file__))


def load_fixture(fixture_name):
    with open(os.path.join(HERE, 'fixtures', fixture_name)) as f:
        return json.loads(f.read())


if sys.version_info.major > 2:
    # mock is part of python3 stdlib
    import sys
    from unittest import mock
    sys.modules['mock'] = mock
