import json

import click
from elasticsearch import Elasticsearch
from escher import __version__
from tabulate import tabulate


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
@click.option('--help', 'needs_help', is_flag=True, default=None)
@click.option('--sort', '-s', 'sort_hints', multiple=True)
@click.option('--verbose', '-v', is_flag=True, default=None)
@click.argument('names', nargs=-1)
@click.pass_context
def aliases(ctx, response_format, local, timeout, hints, needs_help,
            sort_hints, verbose, names):
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
    if needs_help:
        params['help'] = needs_help
    if sort_hints:
        params['s'] = ','.join(sort_hints)
    if verbose:
        params['v'] = verbose
    if names:
        params['name'] = ','.join(names)

    resp_str = client.cat.aliases(**params)
    resp = json.loads(resp_str) if resp_str else {}
    click.echo(tabulate(resp.items()))


cli.add_command(aliases)


def main():
    cli(obj={})
