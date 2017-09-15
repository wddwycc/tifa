import os
import shutil

import click
from jinja2 import Template as JTemplate

from tifa.errors import ValidationError
from tifa.core import Template
from tifa.prompt import Prompt
from tifa.validation import validate_config

here = os.path.abspath(os.path.dirname(__file__))


@click.group()
def main():
    pass


@main.command(help='Generate a tifa configuration yaml')
@click.option('--name', prompt='project name')
def init(name):
    yaml_file = os.path.join(here, 'templates/tifa.example.yaml')
    target_file = './tifa.yaml'
    shutil.copyfile(yaml_file, target_file)
    with open(target_file, 'r+') as f:
        template = JTemplate(f.read())
        content = template.render(name=name) + '\n'
        f.seek(0)
        f.truncate()
        f.write(content)
    Prompt.success('Created tifa.yaml')


@main.command(help='Generate project through configuration')
@click.option(
    '--config', '-c', type=click.Path(exists=True),
    help='Specific configuration file path',
)
@click.option('--factory', '-f', is_flag=True)
def gen(config, factory):
    config_path = config or './tifa.yaml'
    try:
        config = validate_config(config_path)
    except ValidationError as e:
        Prompt.warn(str(e))
        return

    if os.path.isdir(config['name']):
        Prompt.warn('ops, project folder name has been used')
        return

    template = Template(config)
    template.render('./')

    if not factory:
        os.remove(config_path)

    Prompt.success('project {} generated, enjoy coding'.format(config['name']))
