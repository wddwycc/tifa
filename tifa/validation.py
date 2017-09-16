import os

import yaml
from voluptuous import All, Any
from voluptuous import REMOVE_EXTRA
from voluptuous import Required, Optional, Length
from voluptuous import Schema, MultipleInvalid

from tifa.consts import (
    WEBPACK_MODE_DISABLE, WEBPACK_MODE_CLASSIC,
    WEBPACK_MODE_SEPARATE, WEBPACK_MODE_RADICAL
)
from tifa.errors import ValidationError


def _config_schema():
    return Schema({
        Required('name'): All(str, Length(min=1)),
        Optional('routes'): All(list),
        Optional('models'): All(list),
        Optional('confs'): All(list),
        Required('webpack'): Any(
            WEBPACK_MODE_DISABLE, WEBPACK_MODE_CLASSIC,
            WEBPACK_MODE_SEPARATE, WEBPACK_MODE_RADICAL,
        ),
    }, extra=REMOVE_EXTRA)


def normalize_config(config_path):
    if not os.path.isfile(config_path):
        raise ValidationError('no configuration file found')
    with open(config_path, 'r') as f:
        try:
            config = yaml.load(f)
        except Exception:
            raise ValidationError('invalid yaml file')
    schema = _config_schema()
    try:
        config = schema(config)
    except MultipleInvalid:
        raise ValidationError('configuration file invalid')
    config['name'] = config['name'].lower()
    # no space in project name
    if ' ' in config['name']:
        raise ValidationError('space in project name is invalid')
    # validate routes
    routes = config.get('routes')
    if routes:
        for route in routes:
            if ' ' in route or route == '':
                raise ValidationError('invalid route: {}'.format(route))
        routes = [route.lower() for route in routes]
        routes = list(set(routes))
        config['routes'] = routes
    # validate models
    models = config.get('models')
    if models:
        for model in models:
            if ' ' in model or not model[0].isupper() or model == 'Base':
                raise ValidationError('invalid model: {}'.format(model))
        models = list(set(models))
        config['models'] = models
    return config
