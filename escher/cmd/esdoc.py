'''
Define subcommands for 'escat'.
'''

import json

import click
from elasticsearch import Elasticsearch
from escher import __version__
from tabulate import tabulate

ALLOCATION_BYTES_OPTIONS = [
    'b', 'k', 'kb', 'm', 'mb', 'g', 'gb', 't', 'tb', 'p', 'pb'
]


@click.group()
@click.option('--host', '-h', default='localhost')
@click.option('--port', '-p', type=int, default=80)
@click.option('--ssl/--no-ssl', default=False)
@click.version_option(version=__version__, message='escher %(version)s')
@click.pass_context
def cli(ctx, host, port, ssl):
    ctx.obj['host_spec'] = {'host': host, 'port': port, 'use_ssl': ssl}


@click.command()
@click.option('--format', '-f', 'response_format')
@click.option('--local', is_flag=True, default=None)
@click.option('--master-timeout', 'timeout')
@click.option('--hint', '-h', 'hints', multiple=True)
@click.option('--help-api', 'help_api', is_flag=True, default=None)
@click.option('--sort', '-s', 'sort_hints', multiple=True)
@click.option('--verbose', '-v', is_flag=True, default=None)
@click.argument('names', nargs=-1)
@click.pass_context
def index(ctx, response_format, local, timeout, hints, help_api, sort_hints,
          verbose, names):
    host = ctx.obj['host_spec']
    client = Elasticsearch(hosts=[host])
    params = {}
    if response_format:
        params['format'] = response_format
    if local:
        params['local'] = local
    if timeout:
        params['master_timeout'] = timeout
    if hints:
        params['h'] = ','.join(hints)
    if help_api:
        params['help'] = help_api
    if sort_hints:
        params['s'] = ','.join(sort_hints)
    if verbose:
        params['v'] = verbose
    if names:
        params['name'] = ','.join(names)

    resp_str = client.cat.aliases(**params)
    resp = json.loads(resp_str) if resp_str else {}
    click.echo(tabulate(resp.items()))


@click.command()
@click.option('--format', '-f', 'response_format')
@click.option('--local', is_flag=True, default=None)
@click.option('--master-timeout', 'timeout')
@click.option('--node-id', 'node_ids', multiple=True)
@click.option(
    '--bytes', 'bytes_unit', type=click.Choice(ALLOCATION_BYTES_OPTIONS))
@click.option('--hint', '-h', 'hints', multiple=True)
@click.option('--help-api', 'help_api', is_flag=True, default=None)
@click.option('--sort', '-s', 'sort_hints', multiple=True)
@click.option('--verbose', '-v', is_flag=True, default=None)
@click.pass_context
def get(ctx, response_format, local, timeout, node_ids, bytes_unit, hints,
        help_api, sort_hints, verbose):
    host = ctx.obj['host_spec']
    client = Elasticsearch(hosts=[host])
    params = {}
    if response_format:
        params['format'] = response_format
    if local:
        params['local'] = local
    if timeout:
        params['master_timeout'] = timeout
    if node_ids:
        params['node_id'] = ','.join(node_ids)
    if timeout:
        params['bytes'] = bytes_unit
    if hints:
        params['h'] = ','.join(hints)
    if help_api:
        params['help'] = help_api
    if sort_hints:
        params['s'] = ','.join(sort_hints)
    if verbose:
        params['v'] = verbose

    resp_str = client.cat.allocation(**params)
    click.echo(resp_str)


cli.add_command(index)
cli.add_command(get)


def main():
    cli(obj={})
