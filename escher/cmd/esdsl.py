'''
Define subcommands for 'esdsl'.
'''

import json

import click
from escher import __version__


@click.group()
@click.option('--pretty', '-p', is_flag=True)
@click.option('--indent', '-i', type=int)
@click.version_option(version=__version__, message='escher %(version)s')
@click.pass_context
def cli(ctx, pretty, indent):
    if pretty:
        indent = 4
    if indent:
        ctx.obj['indent_size'] = indent


@click.command()
@click.pass_context
def match_none(ctx):
    indent_size = ctx.obj['indent_size']
    resp = json.dumps({"match_none": {}}, indent=indent_size)
    click.echo(resp)


cli.add_command(match_none, name="match-none")


def main():
    cli(obj={})
