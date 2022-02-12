"""
command.py
"""
import re
import sys
import json

from . import format_text
from . import create_json

def setup(subparsers, name, commonOptions):
    """
    Setup subcommand
    """
    global __subcommand__
    __subcommand__ = name

    parser = subparsers.add_parser(__subcommand__, parents=[commonOptions],
                                   help='Display rules with the difference information.')
    parser.set_defaults(func=run)
    parser.add_argument('-i', '--inputfile',
                        help='path to the input text file(exported from original pdf).')
    parser.add_argument('-t', '--type',
                        help='type convert to. text=formatted text, or json=rule data objects.',
                        type=str, choices=['text', 'json'], default='text')


def run(args):
    """
    run subcommand
    """
    #
    # Retrieving textdata
    #
    if args.inputfile is not None:
        with open(args.inputfile, 'r', encoding='UTF-8') as f:
            textdata = f.read()

    elif not sys.stdin.isatty():
        # If the target file is not specified, read it from the pipe.
        # By making sure that the standard input is not 'tty',
        # determine that the standard input is a 'pipe'.
        textdata = sys.stdin.read()

    else:
        print(__subcommand__ + ': error: Missing inputfile ( [-i / --inputfile] is required)')
        sys.exit(1)

    #
    # Getting the Guidelines version
    #
    m = re.search(r"\nAUTOSAR AP Release (\d{2}-\d{2})\n", textdata)
    texttype = m.group(1)

    #
    # Formatting the textdata
    #
    if texttype == "17-10":
        textdata = format_text.format_17_10(textdata)

    elif texttype == "19-03":
        textdata = format_text.format_19_03(textdata)

    else:
        textdata = texttype + " is not supported."

    if args.type == 'text':
        print(textdata)
        exit(0)

    #
    # Creating the rule object
    #
    data = create_json.create_object(textdata)
    print(json.dumps(data, indent=4))
