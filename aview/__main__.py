"""
Command line interface module
"""
import os
import logging
import argparse
import importlib
from . import _CONFIG


def main():
    """
    * Command line interface
    """
    parser = argparse.ArgumentParser(prog=__package__)
    parser.add_argument("-v", "--version", action="store_true", help="show version")

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument('--debug', nargs='*', help='module path to output logger.debug().')

    subparsers = parser.add_subparsers(title='commands')

    here = os.path.dirname(__file__)
    files = os.listdir(os.path.join(here, _CONFIG['app_path']))
    for file in files:
        if os.path.isdir(os.path.join(here, _CONFIG['app_path'], file)) and (file != '__pycache__'):
            importlib.import_module(__package__ + '.' + _CONFIG['app_path'] + '.' + file).setup(subparsers, file, common)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        if hasattr(args, 'debug') and args.debug is not None:
            if len(args.debug) > 0:
                logging.basicConfig()
                for module in args.debug:
                    module = '.'.join(module.split('/'))
                    logging.getLogger(module).setLevel(level=logging.DEBUG)
            else:
                logging.basicConfig(level=logging.DEBUG)

        args.func(args)

    elif args.version:
        print(_CONFIG['version'])

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
