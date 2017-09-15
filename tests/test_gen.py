from tifa.core import File
from tifa.validation import normalize_config


def test_file_render(tmpdir):
    p = tmpdir.join('tifa.yaml')
    file = File(
        name='tifa.yaml', origin='tifa.example.yaml',
        params=dict(name='tifa')
    )
    file.render(tmpdir.strpath)
    normalize_config(p.strpath)


def test_folder_render(tmpdir, template):
    target_folder = tmpdir.join(template.config['name'])
    assert not target_folder.check(dir=1)
    template.render(tmpdir.strpath)
    assert target_folder.check(dir=1)
