import click

from escher import __version__


@click.group()
@click.version_option(version=__version__, message='escher %(version)s')
def cli():
    pass


@click.command()
@click.option('-v', '--verbose', is_flag=True)
def cat(verbose):
    'Call "cat" APIs.'
    click.echo('foo')


cli.add_command(cat)


def main():
    cli()
