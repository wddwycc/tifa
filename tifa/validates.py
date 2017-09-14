import os

import yaml
from voluptuous import Schema, MultipleInvalid
from voluptuous import All
from voluptuous import REMOVE_EXTRA
from voluptuous import Required, Optional, Length

from tifa.errors import ValidationError


def _config_scheme():
    # todo: disable captical of name
    return Schema({
        Required('name'): All(str, Length(min=1)),
        Optional('routes'): All(list),
        Optional('model'): All(list),
    }, extra=REMOVE_EXTRA)


def validate_config(config_path):
    if not config_path:
        config_path = './tifa.yaml'
        if not os.path.isfile(config_path):
            raise ValidationError('No configuration file found')
    with open(config_path, 'r') as f:
        try:
            config = yaml.load(f)
        except Exception:
            raise ValidationError('Cannot load configuration file')
    scheme = _config_scheme()
    try:
        config = scheme(config)
        return config
    except MultipleInvalid:
        raise ValidationError('Configuration file invalid')
