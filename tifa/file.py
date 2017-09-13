import os

from jinja2 import Template as JTemplate

here = os.path.abspath(os.path.dirname(__file__))
_template_root = os.path.join(here, 'templates')


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


class File(object):
    def __init__(self, name, origin, params=None):
        self.name = name
        self.origin = origin
        self.params = params


class Template(Folder):
    pass
