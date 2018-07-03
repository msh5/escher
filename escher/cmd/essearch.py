'''
Define subcommands for 'essearch'.
'''

import json

import click
from elasticsearch import Elasticsearch
from escher import __version__


def build_request_body(queries, aggs):
    body = {}
    if queries:
        body['query'] = []
        for query in queries:
            query_dict = json.dumps(query)
            body['query'].append(query_dict)
    if aggs:
        body['aggs'] = []
        for agg in aggs:
            agg_dict = json.dumps(agg)
            body['aggs'].append(agg_dict)
    return body


@click.command()
@click.option('--host', '-h', default='localhost')
@click.option('--port', '-p', type=int, default=80)
@click.option('--ssl/--no-ssl', default=False)
@click.option('--index', '-i', 'indices', multiple=True)
@click.option('--query', '-q', 'queries', multiple=True)
@click.option('--agg', '-a', 'aggs', multiple=True)
@click.option('--pretty', '-p', is_flag=True)
@click.option('--indent', '-n', 'indent_size', type=int)
@click.version_option(version=__version__, message='escher %(version)s')
def search(host, port, ssl, indices, queries, aggs, pretty, indent_size):
    host_spec = {'host': host, 'port': port, 'use_ssl': ssl}
    client = Elasticsearch(hosts=[host_spec])
    params = {}
    params['index'] = ','.join(indices)
    params['body'] = build_request_body(queries, aggs)
    response = client.search(**params)
    if pretty:
        indent_size = 4
    resp = json.dumps(response, indent=indent_size)
    click.echo(resp)


def main():
    search()
