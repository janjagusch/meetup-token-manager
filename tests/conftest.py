"""
Helper methods for the tests.
"""

import pytest
import yaml


def from_yaml(file_path):
    """
    Reads from a yml file.
    """
    with open(file_path, "r") as file_pointer:
        return yaml.full_load(file_pointer)


@pytest.fixture(scope="module")
def vcr_config():
    """
    vcr_config.
    """
    return {
        "filter_headers": [("Authorization", "XXX")],
    }


@pytest.fixture(name="vcr", scope="module")
def vcr_(vcr):
    """
    vcr.
    """
    vcr.match_on = ["method", "scheme", "port", "path", "body", "query"]
    return vcr


@pytest.fixture(name="token_cache")
def token_cache_():
    """
    An example token from the Redis cache.
    """
    return from_yaml("tests/data/token_cache.yml")
