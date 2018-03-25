import os

import click

from tifa.core import Template, File
from tifa.errors import ValidationError
from tifa.prompt import Prompt
from tifa.validation import normalize_config

here = os.path.abspath(os.path.dirname(__file__))


@click.group()
def main():
    pass


@main.command(help='Generate a tifa configuration yaml')
@click.option('--name', prompt='project name')
def init(name):
    file = File(
        name='tifa.yaml', origin='tifa.example.yaml',
        params=dict(name=name)
    )
    file.render('./')
    Prompt.success('Created tifa.yaml')


@main.command(help='Generate project through configuration')
@click.option(
    '--config', '-c', type=click.Path(exists=True),
    help='Specific configuration file path',
)
def gen(config):
    config_path = config or './tifa.yaml'
    try:
        config = normalize_config(config_path)
    except ValidationError as e:
        Prompt.warn(str(e))
        return

    if os.path.isdir(config['name']):
        Prompt.warn('ops, folder {} has been used'.format(config['name']))
        return

    template = Template(config)
    template.render('./')

    os.remove(config_path)

    Prompt.success('🎉 {} created, enjoy coding!'.format(config['name']))
