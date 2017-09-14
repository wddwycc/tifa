import os
import shutil

import click
from jinja2 import Template as JTemplate

from tifa.errors import ValidationError
from tifa.file import Folder, File, Template
from tifa.filters import under_score
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

    name = config['name']
    routes = config.get('routes')
    db = config.get('db')

    proj_dir = './{}'.format(name)
    if os.path.isdir(proj_dir):
        Prompt.warn('ops, project folder name has been used')
        return

    requirements = [
        'click == 6.7',
        'Flask == 0.12.2',
        'Jinja2 == 2.9.6',
    ]

    # todo: move template gen logic to another file
    module_folders = list()
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
    if db:
        # todo: check same table name & check no name called base
        files = [File(
            name='{}.py'.format(under_score(name)),
            origin='db/table.py.j2',
            params=dict(cls_name=name, table_name=under_score(name))
        ) for name in db]
        files += [
            File(name='__init__.py', origin='db/__init__.py.j2'),
            File(name='base.py', origin='db/base.py.j2'),
        ]
        module_folders.append(Folder(name='model', files=files))
        requirements += [
            'SQLAlchemy==1.1.14',
            'Flask-SQLAlchemy==2.2',
        ]

    module_folder = Folder(
        name=name, sub_folders=module_folders,
        files=[
            File(name='__init__.py', origin='__init__.py.j2', params=dict(
                routes=routes, db=db
            ))
        ]
    )

    # todo 添加conf files
    proj_files = [
        File(name='manage.py', origin='manage.py.j2', params=dict(
            name=name, db=db
        )),
    ]

    proj_folder = Template(
        name=name,
        sub_folders=[module_folder],
        files=proj_files,
        requirements=requirements,
    )

    proj_folder.render('./')
    # todo: remove config file with confidence
    # cli加一個flag, 默認移除yaml file，特殊指定則保留

    Prompt.success('project {} generated, enjoy coding'.format(name))
