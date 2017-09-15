import pytest

from tifa.validation import normalize_config
from tifa.errors import ValidationError


def mock_valid_config():
    return '''
        name: tifa
        routes:
          - front
          - api
        models:
          - User
          - Product
    '''


def mock_bad_name_config():
    return '''
        name: ti fa
    '''


def mock_bad_routes_config():
    return '''
        name: tifa
        routes:
          - fr ont
    '''


def mock_bad_models_config():
    return '''
        name: tifa
        models:
          - Us er
    '''


def test_valid_config(tmpdir):
    p = tmpdir.join('tifa.yaml')
    p.write(mock_valid_config())
    normalize_config(p.strpath)
    assert 1


def test_no_config():
    with pytest.raises(ValidationError,
                       match=r'^no configuration file found$'):
        normalize_config('./nowhere.yaml')


def test_bad_yaml(tmpdir):
    # http://pyyaml.org/wiki/PyYAMLDocumentation#YAMLError
    p = tmpdir.join('tifa.yaml')
    p.write('unbalanced blackets: ][')
    with pytest.raises(ValidationError, match=r'^invalid yaml file$'):
        normalize_config(p.strpath)


def test_bad_name_in_config(tmpdir):
    p = tmpdir.join('tifa.yaml')
    p.write(mock_bad_name_config())
    with pytest.raises(ValidationError,
                       match=r'^space in project name is invalid$'):
        normalize_config(p.strpath)


def test_bad_routes_in_config(tmpdir):
    p = tmpdir.join('tifa.yaml')
    p.write(mock_bad_routes_config())
    with pytest.raises(ValidationError, match=r'^invalid route: .*'):
        normalize_config(p.strpath)


def test_bad_model_in_config(tmpdir):
    p = tmpdir.join('tifa.yaml')
    p.write(mock_bad_models_config())
    with pytest.raises(ValidationError, match=r'^invalid model: .*'):
        normalize_config(p.strpath)
