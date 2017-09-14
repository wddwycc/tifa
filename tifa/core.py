import os

from jinja2 import Template as JTemplate

from tifa.filters import under_score
from tifa.prompt import Prompt

here = os.path.abspath(os.path.dirname(__file__))
_template_root = os.path.join(here, 'templates')

_PY_LIB_VERS = {
    'click': '6.7',
    'Flask': '0.12.2',
    'Jinja2': '2.9.6',
    'SQLAlchemy': '1.1.14',
    'Flask-SQLAlchemy': '2.2',
}


class File(object):
    def __init__(self, name, origin, params=None):
        self.name = name
        self.origin = origin
        self.params = params


class Folder(object):
    def __init__(self, name, sub_folders=None, files=None):
        self.name = name
        self.subfolders = sub_folders
        self.files = files

    def render(self, path):
        sub_folders = self.subfolders
        cursor = os.path.join(path, self.name)
        os.makedirs(cursor)
        if sub_folders:
            for sub_folder in sub_folders:
                sub_folder.render(cursor)
        files = self.files
        if files:
            for file in files:
                template_path = os.path.join(_template_root, file.origin)
                with open(template_path, 'r') as f:
                    template = JTemplate(f.read(), trim_blocks=True)
                if file.params:
                    content = template.render(**file.params)
                else:
                    content = template.render()
                content += '\n'
                file_path = os.path.join(cursor, file.name)
                with open(file_path, 'w') as f:
                    f.write(content)


class Template(object):
    def __init__(self, config):
        self.config = config

    @staticmethod
    def default_requirements():
        return ['click', 'Flask', 'Jinja2']

    def render(self, path):
        config = self.config
        name = config['name']
        routes = config.get('routes')
        model = config.get('model')

        proj_dir = './{}'.format(name)
        if os.path.isdir(proj_dir):
            Prompt.warn('ops, project folder name has been used')
            return

        requirements = Template.default_requirements()

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
        if model:
            # todo: check same table name & check no name called base
            files = [File(
                name='{}.py'.format(under_score(name)),
                origin='model/table.py.j2',
                params=dict(cls_name=name, table_name=under_score(name))
            ) for name in model]
            files += [
                File(name='__init__.py', origin='model/__init__.py.j2',
                     params=dict(model=[(x, under_score(x)) for x in model])),
                File(name='base.py', origin='model/base.py.j2'),
            ]
            module_folders.append(Folder(name='model', files=files))
            requirements += [
                'SQLAlchemy',
                'Flask-SQLAlchemy',
            ]
        module_folder = Folder(
            name=name, sub_folders=module_folders,
            files=[
                File(
                    name='__init__.py', origin='__init__.py.j2',
                    params=dict(routes=routes, model=model),
                )
            ]
        )

        # todo 添加conf files
        proj_files = [
            File(name='manage.py', origin='manage.py.j2', params=dict(
                name=name, model=model
            )),
        ]

        proj_folder = Folder(
            name=name,
            sub_folders=[module_folder],
            files=proj_files
        )

        proj_folder.render(path)
        self.gen_requirements(requirements, path)

    def gen_requirements(self, requirements, path):
        requirements = [x + '==' + _PY_LIB_VERS[x] for x in requirements]
        requirements = '\n'.join(requirements)
        requirements_path = os.path.join(
            path, self.config['name'], 'requirements.txt'
        )
        with open(requirements_path, 'w') as f:
            f.write(requirements + '\n')
