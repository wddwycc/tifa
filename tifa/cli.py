import os
import shutil

import click
import yaml
from jinja2 import Template

from .prompt import Prompt

here = os.path.abspath(os.path.dirname(__file__))


@click.group()
def main():
    pass


@main.command(help='Initialize tifa configuration yaml')
@click.option('--name', prompt='project name')
def init(name):
    Template(name)
    yaml_file = os.path.join(here, 'templates/tifa.example.yaml')
    target_file = './tifa.yaml'
    shutil.copyfile(yaml_file, target_file)
    with open(target_file, 'r+') as f:
        template = Template(f.read())
        content = template.render(name=name) + '\n'
        f.seek(0)
        f.truncate()
        f.write(content)


@main.command(help='Generate project through configuration')
@click.option(
    '--config', type=click.Path(exists=True),
    help='Specific configuration file path',
)
def gen(config):
    config_path = config
    if not config_path:
        config_path = './tifa.yaml'
        if not os.path.isfile(config_path):
            Prompt.warn('No configuration file found')
            return
    with open(config_path, 'r') as f:
        try:
            config = yaml.load(f)
        except Exception as e:
            Prompt.warn(e)
    # todo: move to class
    from voluptuous import Schema, MultipleInvalid
    from voluptuous import All
    from voluptuous import REMOVE_EXTRA
    from voluptuous import Required, Length

    scheme = Schema({
        Required('name'): All(str, Length(min=1))
    }, extra=REMOVE_EXTRA)
    try:
        config = scheme(config)
    except MultipleInvalid:
        Prompt.warn('Configuration file invalid')
        return

    name = config['name']
    # todo: implement configuration
    template_dir = os.path.join(here, 'templates/min')
    proj_dir = './{}'.format(name)
    if os.path.isdir(proj_dir):
        Prompt.warn('ops, folder name has been used')
        return
    shutil.copytree(template_dir, './{}'.format(name))

    def replace_file(file):
        filename = os.path.split(file)[1]
        if filename in ['.DS_Store']:
            return
        with open(file, 'r+') as f:
            template = Template(f.read())
            content = template.render(name=name) + '\n'
            f.seek(0)
            f.truncate()
            f.write(content)
        suffix = filename.split('.')[-1]
        if suffix == 'j2':
            os.rename(file, file.replace('.j2', ''))

    def iter_dir(path):
        for cursor in os.listdir(path):
            cursor_abs = os.path.join(path, cursor)
            if os.path.isdir(cursor_abs):
                if cursor == '<proj>':
                    new_cursor_abs = os.path.join(path, name)
                    os.rename(cursor_abs, new_cursor_abs)
                    cursor_abs = new_cursor_abs
                iter_dir(cursor_abs)
            else:
                replace_file(cursor_abs)

    iter_dir(proj_dir)

    Prompt.success('project {} created, enjoy coding'.format(name))
