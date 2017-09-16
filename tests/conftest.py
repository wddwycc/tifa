import pytest

from tifa.core import Template


@pytest.fixture()
def template():
    """a valid tifa configuration"""
    config = dict(
        name='sample', routes=['front', 'api'],
        models=['User', 'Product'], weppack='classic'
    )
    return Template(config)
