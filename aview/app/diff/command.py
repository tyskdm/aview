"""
command.py
"""
import re
import sys
import json

def setup(subparsers, name, commonOptions):
    """
    Setup subcommand : diff
    """
    global __subcommand__
    __subcommand__ = name

    parser = subparsers.add_parser(__subcommand__, parents=[commonOptions],
                                   help='Converts AUTOSAR text file to json data file')
    parser.set_defaults(func=run)
    parser.add_argument('id', type=str,
                        help='type convert to. text=formatted text, or json=rule data objects.')
    parser.add_argument('-t', '--type',
                        help='type convert to. text=formatted text, or json=rule data objects.',
                        type=str, choices=['text', 'json'], default='text')

    # parser.add_argument('filePath', help='display a square of a given number', nargs='*')
    # parser.add_argument('--upper', help='enable print debug information.', type=int, default=1)
    # parser.add_argument('--lower', help='enable print debug information.', type=int, default=1)
    # parser.add_argument('--long', action='store_true', help='enable print debug information.')
    # parser.add_argument('--verbose', action='store_true', help='enable print debug information.')

# DATA STRUCTURE
# [
#     "A1-1-1": {
#         h "section" = ["", ""]
#         c "class": [],
#         t "rule": "text",
#         n "note": ["", "",...],       # MISRAへの参照もここに含む
#         r "rationale": [],
#         c "exception": [],
#         a "example": [],
#         s "see also": [],
#     }
# ]


_A1710_JSON = "./database/A1710/[17-10]_C++14_Coding_Rules.json"
_A1903_JSON = "./database/A1903/[19-03]_C++14_Coding_Rules.json"

def run(args):
    """
    run subcommand : diff
    """
    #
    # Retrieving json database
    #
    with open(_A1710_JSON, 'r', encoding='UTF-8') as f:
        a1710 = json.load(f)

    with open(_A1903_JSON, 'r', encoding='UTF-8') as f:
        a1903 = json.load(f)

    id = args.id

    if id != "all":

        if id in a1710:
            lines17 = json.dumps(a1710[id], indent=4).split('\n')
            lines17 = ["a17-10: " + x for x in lines17]

            print('\n'.join(lines17))

        else:
            print('not found.\n' + json.dumps(a1710, indent=4))

    else:

        count = 0
        diff_count = 0

        for id in a1710:

            if id.startswith('A'):
                continue

            count += 1

            r17 = a1710[id]
            r19 = a1903[id] if id in a1903 else None

            if r19 is None:
                diff_count += 1

            else:
                if not (r17["rule"] == r19["rule"]):
                    diff_count += 1

        eq_count = count - diff_count

        print("total: " + str(count))
        print("equal: " + str(eq_count))
        print("diff:  " + str(diff_count))

