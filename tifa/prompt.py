import click


def _tint(raw, color):
    return click.style(raw, fg=color)


class Prompt(object):
    @staticmethod
    def warn(raw):
        click.echo(_tint(raw, 'red'))

    @staticmethod
    def success(raw):
        click.echo(_tint(raw, 'green'))
