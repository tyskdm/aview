"""
command.py
"""
import difflib
import json
import re
from xml.dom import EMPTY_NAMESPACE

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
    # parser.add_argument('-t', '--type',
    #                     help='type convert to. text=formatted text, or json=rule data objects.',
    #                     type=str, choices=['text', 'json'], default='text')

    # DATA STRUCTURE
    # [
    #     "A1-1-1": {
    #         h "Section" = ["", ""]
    #         c "Class": [],
    #         t "Rule": "text",
    #         n "Note": ["", "",...],
    #         r "Rationale": [],
    #         c "Exception": [],
    #         a "Example": [],
    #         s "See also": [],
    #     }
    # ]
    parser.add_argument('-H', '--header',     action='store_true', help='Compare section Header')
    parser.add_argument('-C', '--classifier', action='store_true', help='Compare Classifier')
    parser.add_argument('-T', '--text',       action='store_true', help='Compare rule Text')
    parser.add_argument('-N', '--note',       action='store_true', help='Compare Note')
    parser.add_argument('-R', '--rationale',  action='store_true', help='Compare Rationale')
    parser.add_argument('-E', '--exception',  action='store_true', help='Compare Exception')
    parser.add_argument('-X', '--example',    action='store_true', help='Compare eXample')
    parser.add_argument('-S', '--seealso',    action='store_true', help='Compare See also')
    parser.add_argument('-A', '--all',        action='store_true', help='Compare All properties')


_A1710_JSON = "database/A1710/[17-10]_C++14_Coding_Rules.json"
_A1903_JSON = "database/A1903/[19-03]_C++14_Coding_Rules.json"

def run(args):
    """
    run subcommand : diff
    """
    #
    # Retrieving json database
    #
    datadir = '/'.join(__file__.split('/')[:-4]) + '/'  # data directory

    with open(datadir + _A1710_JSON, 'r', encoding='UTF-8') as f:
        a1710 = json.load(f)

    with open(datadir + _A1903_JSON, 'r', encoding='UTF-8') as f:
        a1903 = json.load(f)

    id = args.id
    opts = _set_opts(args)

    if id != "all":

        id_all = a1710.keys() | a1903.keys()
        empty = {
            "Section" : [],
            "Class": [],
            "Rule": "",
            "Note": [],
            "Rationale": [],
            "Exception": [],
            "Example": [],
            "See also": [],
        }

        if id in id_all:
            diff = compare_rule(
                a1710[id] if id in a1710.keys() else empty,
                a1903[id] if id in a1903.keys() else empty,
                opts, all=True
            )

            print("## " + id)
            print("\ndiff: - A17-10 / + A19-03")
            print("-------------------------")
            print("Compare : " + ', '.join(opts["_Compare"]))
            print("Ignore  : " + ', '.join(opts["_Ignore"]))
            print('\n'.join(diff))

        else:
            print('Error: ' + id + ' not found.\n')

    else:
        n_total = len(a1710.keys() | a1903.keys())
        n_common = len(a1710.keys() & a1903.keys())
        n_only_in_17 = len((a1710.keys() ^ a1903.keys()) & a1710.keys())
        n_only_in_19 = len((a1710.keys() ^ a1903.keys()) & a1903.keys())

        print("Total count    = {:>3}".format(n_total))
        print("Common rules   = {:>3}".format(n_common))
        print("Only A17-10    = {:>3}".format(n_only_in_17))
        print("Only A19-03    = {:>3}".format(n_only_in_19))
        print("--------------------")

        common_ids = a1710.keys() & a1903.keys()
        diff_count = 0
        diff_info =[]
        for id in common_ids:
            r17 = a1710[id]
            r19 = a1903[id]

            diff = compare_rule(r17, r19, opts)
            if diff is not None:
                diff_info.append(["\n## " + id] + diff)

        diff_count = len(diff_info)
        eq_count = n_common - diff_count

        print("Same in common = {:>3}".format(eq_count))
        print("diff in common = {:>3}".format(diff_count))
        print("--------------------")

        print("\ndiff: - A17-10 / + A19-03")
        print("-------------------------")
        print("Compare : " + ', '.join(opts["_Compare"]))
        print("Ignore  : " + ', '.join(opts["_Ignore"]))
        for item in diff_info:
            print('\n'.join(item))


# DATA STRUCTURE
# [
#     "A1-1-1": {
#         h "Section" = ["", ""]
#         c "Class": [],
#         t "Rule": "text",
#         n "Note": ["", "",...],
#         r "Rationale": [],
#         c "Exception": [],
#         a "Example": [],
#         s "See also": [],
#     }
# ]
#         L : Loose comparison
def compare_rule(a, b, opts, all = False):

    diffs = []

    all_keys = a.keys() | b.keys()

    if "Section" in all_keys and opts["header"]:
        diff = _diff_lines(
            a["Section"] if "Section" in a.keys() else [],
            b["Section"] if "Section" in b.keys() else [],
            all=all
        )
        if diff:
            diffs += (["\nSection:"] + diff)

    if "Class" in all_keys and opts["classifier"]:
        diff = _diff_lines(
            a["Class"] if "Class" in a.keys() else [],
            b["Class"] if "Class" in b.keys() else [],
            all=all
        )
        if diff:
            diffs += (["\nClass:"] + diff)

    if "Rule" in all_keys and opts["text"]:
        diff = _diff_lines(
            [a["Rule"]] if "Rule" in a.keys() else [],
            [b["Rule"]] if "Rule" in b.keys() else [],
            all=all
        )
        if diff:
            diffs += (["\nRule:"] + diff)

    if "Note" in all_keys and opts["note"]:
        diff = _diff_lines(
            a["Note"] if "Note" in a.keys() else [],
            b["Note"] if "Note" in b.keys() else [],
            all=all
        )
        if diff:
            diffs += (["\nNote:"] + diff)

    if "Rationale" in all_keys and opts["rationale"]:
        diff = _diff_lines(
            a["Rationale"] if "Rationale" in a.keys() else [],
            b["Rationale"] if "Rationale" in b.keys() else [],
            all=all
        )
        if diff:
            diffs += (["\nRationale:"] + diff)

    if "Exception" in all_keys and opts["exception"]:
        diff = _diff_lines(
            a["Exception"] if "Exception" in a.keys() else [],
            b["Exception"] if "Exception" in b.keys() else [],
            all=all
        )
        if diff:
            diffs += (["\nException:"] + diff)

    if "Example" in all_keys and opts["example"]:
        diff = _diff_lines(
            a["Example"] if "Example" in a.keys() else [],
            b["Example"] if "Example" in b.keys() else [],
            all=all
        )
        if diff:
            diffs += (["\nExample:"] + diff)

    if "See also" in all_keys and opts["seealso"]:
        diff = _diff_lines(
            a["See also"] if "See also" in a.keys() else [],
            b["See also"] if "See also" in b.keys() else [],
            all=all
        )
        if diff:
            diffs += (["\nSee also:"] + diff)

    if len(diffs) == 0:
        diffs = None

    return diffs


def _diff_lines(a, b, opt=None, all=False):
    result = None

    text_a = re.sub(r" +", r" ", ' '.join(a))
    text_b = re.sub(r" +", r" ", ' '.join(b))

    if (text_a != text_b) or all:
        result = '\n'.join(difflib.ndiff(a, b)).split('\n')
        result = [a for a in result if a != '']

    return result


def _set_opts(args):
    opts = None

    if args.all:
        opts = {
            "header":       True,
            "classifier":   True,
            "text":         True,
            "note":         True,
            "rationale":    True,
            "exception":    True,
            "example":      True,
            "seealso":      True
        }
    else:
        opts = {
            "header":       args.header,
            "classifier":   args.classifier,
            "text":         args.text,
            "note":         args.note,
            "rationale":    args.rationale,
            "exception":    args.exception,
            "example":      args.example,
            "seealso":      args.seealso
        }
        all_flag = False
        for opt in opts:
            all_flag = all_flag or opts[opt]
        if all_flag is False:
            opts = {
                "header":       False,
                "classifier":   False,
                "text":         True,
                "note":         True,
                "rationale":    True,
                "exception":    True,
                "example":      False,
                "seealso":      False
            }

    _Compare = []
    _Ignore = []
    for opt in opts:
        if opts[opt]:
            _Compare.append(opt)
        else:
            _Ignore.append(opt)

    opts["_Compare"] = _Compare
    opts["_Ignore"] = _Ignore

    return opts
