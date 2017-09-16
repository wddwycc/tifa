import os

from jinja2 import Template as JTemplate

from tifa.filters import under_score
from tifa.consts import PY_LIB_VERS, JS_LIB_VERS
from tifa.consts import (
    WEBPACK_MODE_DISABLE, WEBPACK_MODE_CLASSIC,
    WEBPACK_MODE_SEPARATE, WEBPACK_MODE_RADICAL
)

here = os.path.abspath(os.path.dirname(__file__))
_template_root = os.path.join(here, 'templates')


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

    @property
    def name(self):
        return self.config['name']

    @property
    def routes(self):
        return self.config.get('routes')

    @property
    def models(self):
        return self.config.get('models')

    @property
    def confs(self):
        return self.config.get('confs')

    @property
    def webpack_mode(self):
        return self.config.get('webpack')

    def gen_routes(self):
        routes = self.routes
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
        models = self.models
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

    def gen_confs(self):
        confs = self.confs
        if not confs:
            return None
        files = []
        domain = '<domain>'
        port = '<port>'
        if 'supervisor' in confs:
            files.append(File(
                name='supervisor.conf', origin='conf/supervisor.conf.j2',
                params=dict(name=self.config['name'])
            ))
        if 'gunicorn' in confs:
            files.append(File(
                name='gunicorn_conf.py', origin='conf/gunicorn_conf.py.j2',
                params=dict(port=port)
            ))
        if 'nginx' in confs:
            files.append(File(
                name='nginx.conf', origin='conf/nginx.conf.j2',
                params=dict(domain=domain, port=port)
            ))
        webpack_mode = self.webpack_mode
        # todo: generate webpack files
        if webpack_mode == WEBPACK_MODE_CLASSIC:
            pass
        elif webpack_mode == WEBPACK_MODE_SEPARATE:
            pass
        elif webpack_mode == WEBPACK_MODE_RADICAL:
            pass
        return Folder(name='conf', files=files)

    @staticmethod
    def gen_py_lib_file(libs):
        libs = [x + '==' + PY_LIB_VERS[x] for x in libs]
        return File(
            name='requirements.txt',
            origin='requirements.txt.j2',
            params=dict(libs=libs)
        )

    def gen_js_lib_file(self):
        webpack_mode = self.webpack_mode
        if webpack_mode == WEBPACK_MODE_DISABLE:
            return None
        libs = []
        dev_libs = []
        if webpack_mode == WEBPACK_MODE_CLASSIC:
            dev_libs = ['webpack', 'webpack-dev-server']
        if webpack_mode == WEBPACK_MODE_SEPARATE:
            libs = ['vue']
            dev_libs = [
                'webpack', 'webpack-dev-server',
                'html-webpack-plugin'
            ]
        if webpack_mode == WEBPACK_MODE_RADICAL:
            libs = ['vue']
            dev_libs = ['webpack', 'webpack-dev-server']

        def lib_row(lib):
            return '"' + lib + '": ' + '"' + JS_LIB_VERS[lib] + '"'

        libs = [lib_row(x) for x in libs]
        dev_libs = [lib_row(x) for x in dev_libs]
        return File(
            name='package.json',
            origin='package.json.j2',
            params=dict(libs=libs, dev_libs=dev_libs, name=self.config['name'])
        )

    def gen_src_folder(self):
        pass

    def render(self, path):
        config = self.config
        name = config['name']
        models = config.get('models')
        module_folder, requirements = self.gen_py_module()
        root_folders = [module_folder]
        conf_folder = self.gen_confs()
        if conf_folder:
            root_folders.append(conf_folder)
        manage_file = File(
            name='manage.py', origin='manage.py.j2',
            params=dict(name=name, models=models)
        )
        root_files = [manage_file, self.gen_py_lib_file(requirements)]
        js_lib_file = self.gen_js_lib_file()
        if js_lib_file:
            root_files.append(js_lib_file)
        root = Folder(
            name=name,
            sub_folders=root_folders,
            files=root_files
        )
        root.render(path)
