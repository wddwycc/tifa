import os
import shutil

import click
from jinja2 import Template as JTemplate

from tifa.errors import ValidationError
from tifa.validates import validate_config
from .file import Folder, File, Template
from .prompt import Prompt

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

    name = config['name']
    routes = config.get('routes')
    db = config.get('db')

    proj_dir = './{}'.format(name)
    if os.path.isdir(proj_dir):
        Prompt.warn('ops, project folder name has been used')
        return

    module_folders = []
    if routes:
        files = [File(
            name='{}.py'.format(route),
            origin='routes/route.py.j2',
            params=dict(name=route)
        ) for route in routes]
        files.append(
            File(
                name='__init__.py',
                origin='routes/__init__.py.j2',
                params=dict(routes=routes)
            )
        )
        module_folders.append(Folder(name='routes', files=files))

    root_files = [
        File(name='manage.py', origin='manage.py.j2', params=dict(name=name)),
        File(name='requirements.txt', origin='requirements.txt'),
    ]

    module_folder = Folder(
        name=name, sub_folders=module_folders,
        files=[
            File(name='__init__.py', origin='__init__.py.j2')
        ]
    )

    template = Template(
        name=name,
        sub_folders=[
            module_folder
        ],
        files=root_files)
    template.render('./')
    Prompt.success('project {} generated, enjoy coding'.format(name))
