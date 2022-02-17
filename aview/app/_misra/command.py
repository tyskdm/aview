"""
command.py
"""
import re
import sys
import json

from ...lib import ruledata

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
                        type=str, choices=['text', 'json', 'data'], default='json')

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

    m = re.search(r"^(License terms: .+(\n.+)+)$", textdata, flags=re.MULTILINE)
    LicenseTerms = m.group(1)
    LicenseTerms = LicenseTerms.split('\n')
    for i in range(len(LicenseTerms)):
        while not LicenseTerms[i].endswith('.'):
            LicenseTerms[i] += ' ' + LicenseTerms[i+1]
            del LicenseTerms[i+1]

        if i == len(LicenseTerms) - 1:
            break

    print('\n'.join(LicenseTerms))

    if args.type == 'data':
        print(json.dumps(ruledata.get_misra_data(textdata), indent=4))
        exit(0)

    textdata = ruledata.format_2008(textdata)

    if args.type == 'text':
        print(textdata)
        exit(0)

    data = ruledata.create_object(textdata)

    if args.type == 'json':
        print(json.dumps(data, indent=4))
        exit(0)
