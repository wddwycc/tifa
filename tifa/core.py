import os

from jinja2 import Template as JTemplate

from tifa.filters import under_score

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

    def render(self, path):
        template_path = os.path.join(_template_root, self.origin)
        with open(template_path, 'r') as f:
            template = JTemplate(f.read(), trim_blocks=True)
        if self.params:
            content = template.render(**self.params)
        else:
            content = template.render()
        content += '\n'
        file_path = os.path.join(path, self.name)
        with open(file_path, 'w') as f:
            f.write(content)


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
        if not files:
            return
        for file in files:
            file.render(cursor)


class Template(object):
    def __init__(self, config):
        self.config = config

    @staticmethod
    def default_requirements():
        return ['click', 'Flask', 'Jinja2']

    def gen_routes(self):
        routes = self.config.get('routes')
        if not routes:
            return None
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
        return Folder(name='routes', files=files)

    def gen_models(self):
        models = self.config.get('models')
        if not models:
            return None
        files = [File(
            name='{}.py'.format(under_score(model)),
            origin='model/table.py.j2',
            params=dict(cls_name=model, table_name=under_score(model))
        ) for model in models]
        files += [
            File(name='__init__.py', origin='model/__init__.py.j2',
                 params=dict(models=[(x, under_score(x)) for x in models])),
            File(name='base.py', origin='model/base.py.j2'),
        ]
        # todo: support some default model templates, like user
        return Folder(name='model', files=files)

    def gen_py_module(self):
        requirements = Template.default_requirements()

        module_folders = list()

        model_folder = self.gen_models()
        if model_folder:
            requirements += ['SQLAlchemy', 'Flask-SQLAlchemy']
            module_folders.append(model_folder)

        routes_folder = self.gen_routes()
        if routes_folder:
            module_folders.append(routes_folder)

        config = self.config
        name = config['name']
        routes = config.get('routes')
        models = config.get('models')
        return Folder(
            name=name, sub_folders=module_folders,
            files=[
                File(
                    name='__init__.py', origin='__init__.py.j2',
                    params=dict(routes=routes, models=models),
                )
            ]
        ), requirements

    def gen_requirements(self, requirements, path):
        requirements = [x + '==' + _PY_LIB_VERS[x] for x in requirements]
        requirements = '\n'.join(requirements)
        requirements_path = os.path.join(
            path, self.config['name'], 'requirements.txt'
        )
        with open(requirements_path, 'w') as f:
            f.write(requirements + '\n')

    def render(self, path):
        config = self.config
        name = config['name']
        models = config.get('models')
        module_folder, requirements = self.gen_py_module()
        manage_file = File(
            name='manage.py', origin='manage.py.j2',
            params=dict(name=name, models=models)
        )
        proj_files = [manage_file]
        root_folder = Folder(
            name=name,
            sub_folders=[module_folder],
            files=proj_files
        )
        root_folder.render(path)
        self.gen_requirements(requirements, path)
