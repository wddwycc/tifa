import os
import shutil

import click
from jinja2 import Template as JTemplate

from tifa.errors import ValidationError
from tifa.core import Template
from tifa.prompt import Prompt
from tifa.validates import validate_config

here = os.path.abspath(os.path.dirname(__file__))


@click.group()
def main():
    pass


@main.command(help='Initialize tifa configuration yaml')
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
    '--config', type=click.Path(exists=True),
    help='Specific configuration file path',
)
def gen(config):
    try:
        config = validate_config(config)
    except ValidationError as e:
        Prompt.warn(e.msg)
        return

    template = Template(config)
    template.render('./')

    # todo: remove config file with confidence
    # cli加一個flag, 默認移除yaml file，特殊指定則保留

    Prompt.success('project {} generated, enjoy coding'.format(config['name']))
