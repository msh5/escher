'''
Define subcommands for 'esdsl'.
'''

import json

import click
from escher import __version__


@click.group()
@click.option('--pretty', '-p', is_flag=True)
@click.option('--indent', '-n', type=int)
@click.version_option(version=__version__, message='escher %(version)s')
@click.pass_context
def cli(ctx, pretty, indent):
    if pretty:
        indent = 4
    if indent:
        ctx.obj['indent_size'] = indent


def echo_query(ctx, query):
    indent_size = None
    if 'indent_size' in ctx.obj:
        indent_size = ctx.obj['indent_size']
    resp = json.dumps(query, indent=indent_size)
    click.echo(resp)


@click.command()
@click.option('--boost', '-b', type=float)
@click.pass_context
def match_all(ctx, boost):
    query = {'match_all': {}}
    if boost:
        query['match_all']['boost'] = boost
    echo_query(ctx, query)


@click.command()
@click.pass_context
def match_none(ctx):
    echo_query(ctx, {"match_none": {}})


cli.add_command(match_all, name="match-all")
cli.add_command(match_none, name="match-none")


def main():
    cli(obj={})
