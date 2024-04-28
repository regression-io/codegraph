import argparse
import os
import pprint

from codegraph import __version__, core

def cli():
    parser = argparse.ArgumentParser(prog='CodeGraph', description='Tool that create a graph of code to show dependencies between code entities (methods, classes and etc). CodeGraph does not execute code, it is based only on lex and syntax parse')
    parser.add_argument('-v', '--version', action='version', version=__version__, help="show CodeGraph version")
    parser.add_argument('paths', nargs='*', help="Provide path to code base")
    parser.add_argument('-o', '--object-only', action='store_true', default=False, help="Provide flag if you don't want to visualise your code dependencies as graph")

    args = parser.parse_args()
    main(args)


def main(args):
    usage_graph = core.CodeGraph(args).usage_graph()
    pprint.pprint(usage_graph)
    if not args.object_only:
        # to make more quick work if not needed to visualize
        import codegraph.visualizer as vz
        vz.draw_graph(usage_graph)


if __name__ == '__main__':
    cli()
