"""
command.py
"""
import difflib
import json
import re

from ...lib import ruledata

def setup(subparsers, name, commonOptions):
    """
    Setup subcommand : diff
    """
    global __subcommand__
    __subcommand__ = name

    parser = subparsers.add_parser(__subcommand__, parents=[commonOptions],
                                   help='Converts AUTOSAR text file to json data file')
    parser.set_defaults(func=run)
    parser.add_argument('id', type=str, nargs='*',
                        help='type convert to. text=formatted text, or json=rule data objects.')
    parser.add_argument('-m', '--misra2008',
                        help='path to the misra2008 pdf file.')
    parser.add_argument('-d', '--dump', action='store_true',
                        help='Dump rules specified by ids after diff.')

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

    if args.misra2008 is not None:
        m2008 = ruledata.get_misra_data(args.misra2008)
    else:
        m2008 = None

    rules = {
        "1710": a1710,
        "1903": a1903,
        "2008": m2008
    }

    opts = _set_opts(args)

    #
    # diff ALL
    #
    if args.id[0] == "all":

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

    #
    # diff A17-10 and A19-03
    #
    elif len(args.id) == 1:

        id = args.id[0].split('@')[0]

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

    #
    # diff specified ids
    #
    else:
        (ida, idb) = _set_id(args.id)

        if "2008" in (ida[1], idb[1]) and rules["2008"] is None:
            print(__subcommand__ + ': error: Missing inputfile([-m/--misra2008] is required)')

        if ida[0] not in rules[ida[1]].keys():
            print('Error: ' + args.id[0] + ' not found.\n')
            exit(1)

        if idb[0] not in rules[idb[1]].keys():
            print('Error: ' + args.id[1] + ' not found.\n')
            exit(1)

        rule_a = rules[ida[1]][ida[0]]
        rule_b = rules[idb[1]][idb[0]]

        diff = compare_rule(rule_a, rule_b, opts, all=True)

        if args.dump:
            print("### Diff\n")
            print("```text")

        headline = "diff: - " + ida[0]+"@"+ida[1] + " / + " + idb[0]+"@"+idb[1]
        print(headline)
        print("-" * len(headline))
        print("Compare : " + ', '.join(opts["_Compare"]))
        print("Ignore  : " + ', '.join(opts["_Ignore"]))
        print('\n'.join(diff))

        if args.dump:
            print("```\n")
            dump_rules(
                (ida[0]+"@"+ida[1], rule_a),
                (idb[0]+"@"+idb[1], rule_b),
                opts, all=True
            )


def _set_id(ids):

    ida = ids[0].split('@')
    ida[0] = ida[0].upper()

    if len(ida) == 1:
        if ida[0].startswith(('A', 'M')):
            ida.append('1710')
        else:
            ida.append('2008')

    elif ida[1].startswith('17'):
        ida[1] = '1710'
    elif ida[1].startswith('19'):
        ida[1] = '1903'
    elif ida[1].endswith('08'):
        ida[1] = '2008'
    else:
        print("Invalid id option: " + ids[0])
        exit(1)

    idb = ids[1].split('@')
    idb[0] = idb[0].upper()

    if len(idb) == 1:
        if idb[0].startswith(('A', 'M')):
            idb.append('1903')
        else:
            idb.append('2008')

    elif idb[1].startswith('17'):
        idb[1] = '1710'
    elif idb[1].startswith('19'):
        idb[1] = '1903'
    elif idb[1].endswith('08'):
        idb[1] = '2008'
    else:
        print("Invalid id option: " + ids[0])
        exit(1)

    return (ida, idb)


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


def dump_rules(a, b, opts, all = False):
    dump_rule(a, opts, all)
    dump_rule(b, opts, all)


def dump_rule(dumprule, opts, all = False):

    name = dumprule[0]
    rule = dumprule[1]

    print("\n### " + name)

    all_keys = rule.keys()

    if "Section" in all_keys and opts["header"]:
        print("\n#### Section")
        print("\n" + "\n".join(rule["Section"]))

    if "Class" in all_keys and opts["classifier"]:
        print("\n#### Class")
        print("\n" + "\n".join(rule["Class"]))

    if "Rule" in all_keys and opts["text"]:
        print("\n#### Rule")
        print("\n" + rule["Rule"])

    if "Note" in all_keys and opts["note"]:
        print("\n#### Note")
        print("\n" + "\n".join(rule["Note"]))

    if "Rationale" in all_keys and opts["rationale"]:
        print("\n#### Rationale")
        print("\n" + "\n".join(rule["Rationale"]))

    if "Exception" in all_keys and opts["exception"]:
        print("\n#### Exception")
        print("\n" + "\n".join(rule["Exception"]))

    if "Example" in all_keys and opts["example"]:
        print("\n#### Example")
        print("\n" + "\n".join(rule["Example"]))

    if "See also" in all_keys and opts["seealso"]:
        print("\n#### See also")
        print("\n" + "\n".join(rule["See also"]))

