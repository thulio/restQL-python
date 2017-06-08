import sys


if sys.version_info.major > 2:
    # mock is part of python3 stdlib
    import sys
    from unittest import mock
    sys.modules['mock'] = mock
