from xml.etree import ElementTree

import bonobo

from .indexing import index_biblio, index_clms
from .parsing import *


def split_file(fname):
    """Splits a standard USPTO XML grant file into single grant documents

    A single USPTO XML file contains thousands of XML documents, so iterparse throws errors.
    Using a simple pattern matching rule to identify first line of a doc so we can split.

    Args:
        * fname: (str) USPTO XML grant file

    Returns:
        A dictionary containing the following:
            * 'raw': (str) Fully-formed valid XML documnent

    """
    STOPPER = '<?xml version="1.0" encoding="UTF-8"?>\n'

    buffer = ''
    with open(fname, 'r') as fin:
        for line in fin:
            if buffer and line == STOPPER:
                yield {'raw': buffer}
                buffer = ''
            buffer += line
        yield {'raw': buffer}


def parse_grant_components(d):
    # TODO - Add sanity checks!
    root = get_xml_root(d.get('raw'))
    biblio = parse_biblio(root)
    yield {
        **d,
        'docid': '{}{}'.format(biblio.get('ap_iso'), biblio.get('ap_no')),
        'biblio': biblio,
        'clms': parse_clms(root)
    }


def print_info(d):
    print(d.get('biblio'), d.get('clms'))


def load(d):
    # TODO - Add sanity checks!
    if d.get('biblio'):
        index_biblio(d.get('docid'), d.get('biblio'))
        index_clms(d.get('docid'), d.get('clms'))


def get_graph(**options):
    graph = bonobo.Graph()
    graph.add_chain(
        split_file(options.get('fname')),
        parse_grant_components,
        load)
    return graph


def get_services(**options):
    return {}


if __name__ == '__main__':
    parser = bonobo.get_argument_parser()
    parser.add_argument('fname', type=str)

    with bonobo.parse_args(parser) as options:
        bonobo.run(
            get_graph(**options),
            services=get_services(**options)
        )