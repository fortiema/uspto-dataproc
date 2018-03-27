# -*- coding: utf-8 -*-

"""Console script for uspto_data_processor."""

import click

from . import crawling


@click.group()
def cli():
    pass

@cli.command()
@click.argument('year')
def crawl(year):
    crawling.main(year)


if __name__ == "__main__":
    cli()
