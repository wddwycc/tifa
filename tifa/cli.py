import os
import shutil
from .prompt import Prompt

import click


@click.group()
def main():
    pass


@main.command('min')
@click.option('--name', prompt='project name')
def proj_min(name):
    from jinja2 import Template

    here = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(here, 'templates/min')

    proj_dir = './{}'.format(name)
    if os.path.isdir(proj_dir):
        Prompt.warn('ops, folder name has been used')
        return
    shutil.copytree(template_dir, './{}'.format(name))

    def replace_file(file):
        print(file)
        filename = os.path.split(file)[1]
        suffix = filename.split('.')[-1]
        with open(file, 'r+') as f:
            template = Template(f.read())
            content = template.render(name=name) + '\n'
            f.seek(0)
            f.truncate()
            f.write(content)
        if suffix == 'j2':
            os.rename(file, file.replace('.j2', '.py'))

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
