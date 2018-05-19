import click

from escher import __version__
from elasticsearch import Elasticsearch
from tabulate import tabulate


@click.group()
@click.option('--host', '-h', default='localhost')
@click.option('--port', '-p', type=int, default='80')
@click.option('--ssl/--no-ssl', default=False)
@click.version_option(version=__version__, message='escher %(version)s')
@click.pass_context
def cli(ctx, host, port, ssl):
    ctx.obj['host_spec'] = {'host': host, 'port': port, 'use_ssl': ssl}


@click.command()
@click.pass_context
def health(ctx):
    '''Check cluster health'''
    host = ctx.obj['host_spec']
    client = Elasticsearch(hosts=[host])
    resp = client.cluster.health()
    click.echo(tabulate(resp.items()))


cli.add_command(health)


def main():
    cli(obj={})
