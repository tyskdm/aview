"""
command.py
"""
from cgitb import text
import json
import logging
import re
import sys
from ...lib import debug

_LOGGER = logging.getLogger(__name__)
_DEBUG = debug.Debug(_LOGGER)

def setup(subparsers, name, commonOptions):
    """
    Setup subcommand
    """
    global __subcommand__
    __subcommand__ = name

    parser = subparsers.add_parser(__subcommand__, parents=[commonOptions], help='Converts AUTOSAR text file to json data file')
    parser.set_defaults(func=run)
    parser.add_argument('-i', '--inputfile', help='path to the exported text file.')


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
        textdata = format_17_10(textdata)

    elif texttype == "19-03":
        textdata = format_19_03(textdata)

    else:
        textdata = texttype + " is not supported."

    print(textdata)


def format_17_10(textdata) -> str:
    _TOC_ = [
        ["AUTOSAR C++14 coding rules", "6"],
        ["Language independent issues", "6.0"],
        ["Unnecessary constructs", "6.0.1"],
        ["Storage", "6.0.2"],
        ["Runtime failures", "6.0.3"],
        ["Arithmetic", "6.0.4"],
        ["General", "6.1"],
        ["Scope", "6.1.1"],
        ["Normative references", "6.1.2"],
        ["Implementation compliance", "6.1.4"],
        ["Lexical conventions", "6.2"],
        ["Character sets", "6.2.3"],
        ["Trigraph sequences", "6.2.5"],
        ["Alternative tokens", "6.2.6"],
        ["Comments", "6.2.8"],
        ["Header names", "6.2.9"],
        ["Identifiers", "6.2.11"],
        ["Literals", "6.2.14"],
        ["Basic concepts", "6.3"],
        ["Declarations and definitions", "6.3.1"],
        ["One Definition Rule", "6.3.2"],
        ["Scope", "6.3.3"],
        ["Name lookup", "6.3.4"],
        ["Types", "6.3.9"],
        ["Standard conversions", "6.4"],
        ["Integral promotions", "6.4.5"],
        ["Integral conversion", "6.4.7"],
        ["Pointer conversions", "6.4.10"],
        ["Expressions", "6.5"],
        ["General", "6.5.0"],
        ["Primary expression", "6.5.1"],
        ["Postfix expressions", "6.5.2"],
        ["Unary expressions", "6.5.3"],
        ["Multiplicative operators", "6.5.6"],
        ["Shift operators", "6.5.8"],
        ["Equality operators", "6.5.10"],
        ["Logical AND operator", "6.5.14"],
        ["Conditional operator", "6.5.16"],
        ["Assignment and compound assignment operation", "6.5.18"],
        ["Comma operator", "6.5.19"],
        ["Constant expression", "6.5.20"],
        ["Statements", "6.6"],
        ["Expression statement", "6.6.2"],
        ["Compound statement or block", "6.6.3"],
        ["Selection statements", "6.6.4"],
        ["Iteration statements", "6.6.5"],
        ["Jump statements", "6.6.6"],
        ["Declaration", "6.7"],
        ["Specifiers", "6.7.1"],
        ["Enumeration declaration", "6.7.2"],
        ["Namespaces", "6.7.3"],
        ["The asm declaration", "6.7.4"],
        ["Linkage specification", "6.7.5"],
        ["Declarators", "6.8"],
        ["General", "6.8.0"],
        ["Ambiguity resolution", "6.8.2"],
        ["Meaning of declarators", "6.8.3"],
        ["Function definitions", "6.8.4"],
        ["Initializers", "6.8.5"],
        ["Classes", "6.9"],
        ["Member function", "6.9.3"],
        ["Unions", "6.9.5"],
        ["Bit-fields", "6.9.6"],
        ["Derived Classes", "6.10"],
        ["Multiple base Classes", "6.10.1"],
        ["Member name lookup", "6.10.2"],
        ["Virtual functions", "6.10.3"],
        ["Member access control", "6.11"],
        ["General", "6.11.0"],
        ["Friends", "6.11.3"],
        ["Special member functions", "6.12"],
        ["General", "6.12.0"],
        ["Constructors", "6.12.1"],
        ["Destructors", "6.12.4"],
        ["Initialization", "6.12.6"],
        ["Construction and destructions", "6.12.7"],
        ["Copying and moving class objects", "6.12.8"],
        ["Overloading", "6.13"],
        ["Overloadable declarations", "6.13.1"],
        ["Declaration matching", "6.13.2"],
        ["Overload resolution", "6.13.3"],
        ["Overloaded operators", "6.13.5"],
        ["Build-in operators", "6.13.6"],
        ["Templates", "6.14"],
        ["General", "6.14.0"],
        ["Template parameters", "6.14.1"],
        ["Template declarations", "6.14.5"],
        ["Name resolution", "6.14.6"],
        ["Template instantiation and specialization", "6.14.7"],
        ["Function template specializations", "6.14.8"],
        ["Exception handling", "6.15"],
        ["General", "6.15.0"],
        ["Throwing an exception", "6.15.1"],
        ["Constructors and destructors", "6.15.2"],
        ["Handling an exception", "6.15.3"],
        ["Exception specifications", "6.15.4"],
        ["Special functions", "6.15.5"],
        ["Preprocessing directives", "6.16"],
        ["General", "6.16.0"],
        ["Conditional inclusion", "6.16.1"],
        ["Source file inclusion", "6.16.2"],
        ["Macro replacement", "6.16.3"],
        ["Error directive", "6.16.6"],
        ["Pragma directive", "6.16.7"],
        ["Library introduction - partial", "6.17"],
        ["General", "6.17.1"],
        ["The C standard library", "6.17.2"],
        ["Definitions", "6.17.3"],
        ["Language support library - partial", "6.18"],
        ["General", "6.18.0"],
        ["Types", "6.18.1"],
        ["Implementation properties", "6.18.2"],
        ["Dynamic memory management", "6.18.5"],
        ["Other runtime support", "6.18.9"],
        ["Diagnostics library - partial", "6.19"],
        ["Error numbers", "6.19.4"],
        ["Containers library - partial", "6.23"],
        ["General", "6.23.1"],
        ["Input/output library - partial", "6.27"],
        ["General", "6.27.1"]
    ]

    # Remove page num
    textdata = re.sub(r"(^\n)*\d{2,3} of \d{3}\n(^\n)*", "", textdata, flags=re.MULTILINE)

    # Remove footer
    textdata = re.sub(r"(^\n)*Document ID 839: AUTOSAR_RS_CPP14Guidelines\n— AUTOSAR CONFIDENTIAL —\n(^\n)*[^G]",
                       "", textdata, flags=re.MULTILINE)

    # Remove header
    textdata = re.sub(r"(^\n)*^Guidelines for the use of the C\+\+14 language in critical and safety-related systems\nAUTOSAR AP Release \d{2}-\d{2}\n(^\n)*",
                       "", textdata, flags=re.MULTILINE)

    # Table 6.1
    # Issue: Solution: Correctness of the exception handling
    textdata = re.sub(r"^(Issue:)\n+(Solution:)\n+(Correctness of the exception handling)$",
                      r"\n\1\n\n\2\n\n\3\n", textdata, flags=re.MULTILINE)
    # Exception safety and
    textdata = re.sub(r"^(Exception)\n+(safety)\n+(and)$",
                      r"\n\1 \2 \3", textdata, flags=re.MULTILINE)

    # Part header
    textdata = re.sub(r"(^(Rationale|Exception|Example|See also)$)",
                      r"\n##### \1\n", textdata, flags=re.MULTILINE)

    textdata = re.sub(r"(^See MISRA C\+\+ 2008\s\[\d+\])$",
                      r"\n\1\n", textdata, flags=re.MULTILINE)

    textdata = re.sub(r"(^See:)",
                      r"\n\1", textdata, flags=re.MULTILINE)

    textdata = re.sub(r"(^Note:)",
                      r"\n\1", textdata, flags=re.MULTILINE)

    # List and sublist
    # textdata = re.sub(r"^– (.+)$",
    #                   r"\n  - \1\n", textdata, flags=re.MULTILINE)
    # textdata = re.sub(r"(^• )",
    #                   r"\n- ", textdata, flags=re.MULTILINE)
    textdata = re.sub(r"^– (.+)$",
                      r"\n\1\n", textdata, flags=re.MULTILINE)
    textdata = re.sub(r"(^• )",
                      r"\n", textdata, flags=re.MULTILINE)

    textdata = re.sub(r"(^Rule \D\d{1,2}-\d{1,2}-\d{1,2} \(.+?, .+?, .+?\))\n(.+$)(\n(.+$))?(\n(.+$))?(\n(.+$))?(\n(.+$))?(\n(.+$))?",
                      r"\n#### \1<br>\2 \4 \6 \8 \10 \12\n", textdata, flags=re.MULTILINE)

    textdata = re.sub(r"(^##### Example\n+)(\s*(1|//|//%)\s.*\n(.*\n)*?)(\n)*?##",
                      r"\1```cpp\n\2```\n\n##", textdata, flags=re.MULTILINE)

    textdata = re.sub(r" +$", "", textdata, flags=re.MULTILINE)

    ###############################################################################
    # Line specific detailed replacements
    #
    textdata = re.sub(r"(floating-point data\ntype:\n)((.*\n)*?)\n##",
                      r"\1\n\n```cpp\n\2```\n\n##", textdata, flags=re.MULTILINE)

    textdata = re.sub(r"(Running out of memory)\n(Custom memory management functions)",
                      r"\1\n\n\2", textdata, flags=re.MULTILINE)

    textdata = re.sub(r"^(Note that in most automotive applications,)",
                      r"\n\1", textdata, flags=re.MULTILINE)

    textdata = re.sub(r"^(In place of dynamic exception-specification,)",
                      r"\n\1", textdata, flags=re.MULTILINE)

    textdata = re.sub(r"^(1\. )",
                      r"\n\1", textdata, flags=re.MULTILINE)

    textdata = re.sub(r"^(Advantages of using exceptions)$",
                      r"\n**\1**\n", textdata, flags=re.MULTILINE)

    textdata = re.sub(r"^(Challenges of using exceptions)$",
                      r"\n**\1**\n", textdata, flags=re.MULTILINE)

    textdata = re.sub(r"^(Challenges arising due to dynamic memory usage)$",
                      r"\n**\1**\n", textdata, flags=re.MULTILINE)

    # LineBreak after reference.
    textdata = re.sub(r"(\[\d+\]\])$",
                      r"\1\n", textdata, flags=re.MULTILINE)

    # Table 6.1
    textdata = re.sub(r"^(Maturity of exceptions)$",
                      r"\n\1\n", textdata, flags=re.MULTILINE)

    # Table 6.1
    textdata = re.sub(r"^Appropriate usage\simplementation\n+of\n+exceptions\n+in$",
                      r"\nAppropriate usage of exceptions in implementation\n", textdata, flags=re.MULTILINE)

    # Remove
    textdata = re.sub(r"^——————————————————————————\n",
                      r"", textdata, flags=re.MULTILINE)

    textdata = re.sub(
        r"C\+\+ Core Guidelines \[10\]:\n+shared_ptrs\.\n+R\.24:\n+Use std::weak_ptr to break cycles of",
        r"C++ Core Guidelines [10]: R.24: Use std::weak_ptr to break cycles of shared_ptrs.", textdata, flags=re.MULTILINE)

    # Rule A16-2-1: Rationale
    textdata = re.sub(
        r"It is undefined behavior if the.+\n(.*\n)*?characters are used in #include$",
        r"It is undefined behavior if the ’, " + '"' + r", //, \\\\ characters are used in #include directive, between < and > or “ ” delimiters.\n", textdata, flags=re.MULTILINE)

    # Rule A13-1-1: Rationale
    textdata = re.sub(
        r"(^- const char32_t\*, std::size_t)$",
        r"\1\n", textdata, flags=re.MULTILINE)

    # Rule A18-9-2: See also
    textdata = re.sub(
        r"^(- Effective Modern C\+\+ \[12\]: Item 25\.)\n+" +
        r"(std::forward on universal references\.)\n+" +
        r"(Use std::move on rvalue references,)$",

        r"\1 \3 \2", textdata, flags=re.MULTILINE)
    #
    ###############################################################################

    lines = textdata.split('\n')
    line_idx = 0
    for header in _TOC_:
        for i in range(line_idx, len(lines)):
            if header[0] == lines[i]:
                lines[i] = (
                    '\n' + ("#" * len(header[1].split('.'))) + " "
                    + header[1] + " " + lines[i] + '\n'
                )
                line_idx = i + 1
                break

        if i == len(lines):
            print("TOC '" + header[0] + "' not found.")
            break

    textdata = '\n'.join(lines[2:])
    textdata = re.sub(r"\n\n\n*", "\n\n", textdata, flags=re.MULTILINE)

    textdata = concatenate_lines(textdata)
    textdata = remove_reference_num(textdata)

    return textdata


def format_19_03(textdata) -> str:

    # Remove page num
    textdata = re.sub(r"(^\n)*\d{2,3} of \d{3}\n(^\n)*", "", textdata, flags=re.MULTILINE)

    # Remove footer
    textdata = re.sub(r"(^\n)*Document ID 839: AUTOSAR_RS_CPP14Guidelines\n*?.?— AUTOSAR CONFIDENTIAL —\n(^\n)*[^G]",
                       "", textdata, flags=re.MULTILINE)

    # Remove header
    textdata = re.sub(r"(^\n)*^.?Guidelines for the use of the C\+\+14 language( |\n)in( |\n)critical and safety-related systems\nAUTOSAR AP Release \d{2}-\d{2}\n(^\n)*",
                       "", textdata, flags=re.MULTILINE)

    # Table 6.1
    # Issue: Solution: Correctness of the exception handling
    textdata = re.sub(r"^(Issue:)\n+(Solution:)\n+(Correctness of the exception handling)$",
                      r"\n\1\n\n\2\n\n\3\n", textdata, flags=re.MULTILINE)
    # Exception safety and
    textdata = re.sub(r"^(Exception)\n+(safety)\n+(and)$",
                      r"\n\1 \2 \3", textdata, flags=re.MULTILINE)

    # Part header
    textdata = re.sub(r"(^(Rationale|Exception|Example|See also)$)",
                      r"\n##### \1\n", textdata, flags=re.MULTILINE)

    textdata = re.sub(r"(^See MISRA C\+\+ 2008\s\[\d+\])$",
                      r"\n\1\n", textdata, flags=re.MULTILINE)

    textdata = re.sub(r"(^See:)",
                      r"\n\1", textdata, flags=re.MULTILINE)

    textdata = re.sub(r"(^Note:)",
                      r"\n\1", textdata, flags=re.MULTILINE)

    # List and sublist: 19-03 doesn't use this style. 
    # textdata = re.sub(r"^– (.+)$",
    #                   r"\n  - \1\n", textdata, flags=re.MULTILINE)
    # textdata = re.sub(r"(^• )",
    #                   r"\n- ", textdata, flags=re.MULTILINE)

    textdata = re.sub(r"^(Rule (A|M)\d{1,2}-\d{1,2}-\d{1,2} \((required,|advisory,).+)\n(.+$)(\n(.+$))?(\n(.+$))?(\n(.+$))?(\n(.+$))?(\n(.+$))?",
                      r"\n#### \1 \4 \6 \8 \10 \12 \14\n", textdata, flags=re.MULTILINE)
    # Rule M4-5-1:
    textdata = re.sub(r"(operators &&, \|\|, !,)\s*\n+(the equality operators == and.+)\n(.+)$",
                      r"\1 \2 \3", textdata, flags=re.MULTILINE)
    # split lines
    textdata = re.sub(r"^(#### Rule (A|M)\d{1,2}-\d{1,2}-\d{1,2} \((required,|advisory,).+?\))\s(\S.+)$",
                      r"\1<br>\4", textdata, flags=re.MULTILINE)

    textdata = re.sub(r"(^##### Example\n+)(\s*(1|//|//%)\s.*\n(.*\n)*?)(\n)*?##",
                      r"\1```cpp\n\2```\n\n##", textdata, flags=re.MULTILINE)

    textdata = re.sub(r" +$", "", textdata, flags=re.MULTILINE)

    ###############################################################################
    # Line specific detailed replacements
    #
    textdata = re.sub(r"(floating-point\ndata type:\n)((.*\n)*?)\n##",
                      r"\1\n\n```cpp\n\2```\n\n##", textdata, flags=re.MULTILINE)
    textdata = re.sub(r"(Returning from such a function leads to undefined behavior\.\n)((.*\n)*?)\n##",
                      r"\1\n\n```cpp\n\2```\n\n##", textdata, flags=re.MULTILINE)

    # Rule A18-5-5: Rationale - Recheck around this line.
    textdata = re.sub(r"(Running out of memory)\n(Custom memory management functions)",
                      r"\1\n\n\2", textdata, flags=re.MULTILINE)

    textdata = re.sub(r"^(Note that in most automotive applications,)",
                      r"\n\1", textdata, flags=re.MULTILINE)

    # Recheck around this line.
    textdata = re.sub(r"^(In place of dynamic exception-specification,)",
                      r"\n\1", textdata, flags=re.MULTILINE)

    textdata = re.sub(r"^(1\. )",
                      r"\n\1", textdata, flags=re.MULTILINE)

    # 6.15 Exception handling
    textdata = re.sub(r"^(Advantages of using exceptions)$",
                      r"\n**\1**\n", textdata, flags=re.MULTILINE)
    textdata = re.sub(r"^(Challenges of using exceptions)$",
                      r"\n**\1**\n", textdata, flags=re.MULTILINE)

    # 6.18.5 Dynamic memory management
    textdata = re.sub(r"^(Challenges arising due to dynamic memory usage)$",
                      r"\n**\1**\n", textdata, flags=re.MULTILINE)

    # LineBreak after reference.
    textdata = re.sub(r"(\[\d+\]\])$",
                      r"\1\n", textdata, flags=re.MULTILINE)

    # # Table 6.1:
    # textdata = re.sub(r"^(Maturity of exceptions)$",
    #                   r"\n\1\n", textdata, flags=re.MULTILINE)

    # Rule A18-9-2: See also
    textdata = re.sub(
        r"^(Effective Modern C\+\+ \[13\]: Item 25\.)",
        r"\n\1", textdata, flags=re.MULTILINE)

    # Rule A15-4-1: See also
    textdata = re.sub(
        r"^(open-std\.org \[18\]: open std Deprecating Exception Specifications)",
        r"\n\1", textdata, flags=re.MULTILINE)
    textdata = re.sub(
        r"^(mill22: A Pragmatic Look at Exception Specifications)",
        r"\n\1", textdata, flags=re.MULTILINE)

    # Rule A7-1-6: See also
    textdata = re.sub(
        r"^(C\+\+ Standard Core Language Active Issues, Revision 96 \[18\]:)",
        r"\n\1", textdata, flags=re.MULTILINE)

    # Effective Java 2nd Edition [15]
    textdata = re.sub(
        r"^(Effective Java 2nd Edition \[15\]:)",
        r"\n\1", textdata, flags=re.MULTILINE)

    # Rule A15-0-1: See also
    # 
    textdata = re.sub(
        r"^(The C\+\+ Programming Language \[14\], 13\.1\.1\. Exceptions)",
        r"\n\1", textdata, flags=re.MULTILINE)
    #
    ###############################################################################

    # Section header
    textdata = re.sub(
        r"^(6\.\d{1,2}\.\d{1,2} .+)$",
        r"\n### \1\n", textdata, flags=re.MULTILINE)

    textdata = re.sub(
        r"^(6\.\d{1,2} .+)$",
        r"\n## \1\n", textdata, flags=re.MULTILINE)

    textdata = re.sub(
        r"^(6 AUTOSAR C\+\+14 coding rules)$",
        r"\n# \1\n", textdata, flags=re.MULTILINE)

    textdata = re.sub(r"\n\n\n*", "\n\n", textdata, flags=re.MULTILINE)

    textdata = concatenate_lines(textdata)
    textdata = remove_reference_num(textdata)

    return textdata


def concatenate_lines(textdata):

    lines = textdata.split('\n')
    i = 0
    while i < len(lines)-1:
        if re.match("^#+ ", lines[i]):
            lines[i] = lines[i].replace(' / ', '/')
            i += 1
            continue

        if re.match("^```cpp$", lines[i]):
            i += 1
            while lines[i] != "```":
                if lines[i] == "":
                    del lines[i]
                    continue # without increment
                elif re.match(r"^\d{1,3}$", lines[i]) is not None:
                    del lines[i]
                    continue # without increment

                # A\d{1,3}-\d{1,3}-\d{1,3}\.(cpp|hpp)
                if re.search(r"(A|M)\d{1,3}-\d{1,3}-\d{1,3}\.(cpp|hpp)[^\"]", lines[i]) is None:
                    del lines[i]
                    continue # without increment

                i += 1
            i += 1
            continue

        if lines[i] != "":
            while (
                    (not lines[i].endswith(".")) and
                    (lines[i+1] != "") and
                    (not re.match("^\s*\d+\. ", lines[i+1]))
                ):
                lines[i] = lines[i] + ' ' + lines[i+1]
                del lines[i+1]
            
            if lines[i+1] != "":
                lines.insert(i+1, "")

        i += 1

    textdata = '\n'.join(lines)

    return textdata


def remove_reference_num(textdata):

    textdata = re.sub(r"((" +
            r"MISRA C\+\+ 2008|" +
            r"HIC\+\+ v4\.0|" +
            r"JSF December 2005|" +
            r"SEI CERT C\+\+|" +
            r"C\+\+ Core Guidelines|" +
            r"ISO 26262-6|" +
            r"Google C\+\+ Style Guide|" +          # 17[11], 19[12]
            r"Effective Modern C\+\+|" +            # 17[12], 19[13]
            r"The C\+\+ Programming Language|" +    # 17[13], 19[14]
            r"Effective Java 2nd Edition|" +        # 17[14], 19[15]
            r"stackoverflow\.com|" +                # 17[16], 19[17]
            r"SEI CERT C\+\+ Coding Standard" +
        r")\s\[)\d{1,2}(\])",
        r"\1 \3", textdata)

    # 17-10[3], 19-10[3]
    # ISO/IEC 14882:2014, ISO International Standard ISO/IEC 14882:2014(E) -
    # Programming Language C++, International Organization for Standardization, 2016.
    textdata = re.sub(r"((" +
            r"C\+\+14 Language Standard|" +
            r"\[C\+\+14 Language Standard\]|" +
            r"C\+\+ Language Standard|" +
            r"ISO/IEC 14882:2014" +
        r")\s\[)\d{1,2}(\])",
        r"\1 \3", textdata)

    # 17-10[5], 19-10[6]
    # ISO 26262-8, Road vehicles - Functional safety - Part 8: Supporting processes,
    # International Organization for Standardization, 2011.
    textdata = re.sub(r"((" +
            r"ISO 26262 standard|" +
            r"ISO 26262-8\.11\.4\.6|" +
            r"ISO 26262-8" +
        r")\s\[)\d{1,2}(\])",
        r"\1 \3", textdata)

    # 17-10[15], 19-10[16]
    # cppreference.com, online reference for the C and C++ languages and standard
    # libraries, 2017
    textdata = re.sub(r"((" +
            r"cppreference\.com|" +
            r"CppReference|" +
            r"if the enumeration satisfies the “BitmaskType” concept|" +
            r"See: Using-directive|" +
            r"See: Using-declaration|" +
            r"std::terminate\(\) in CppReference|" +
            r"See: std::stoi, std::stol, std::stoll|" +
            r"see: std::stoi\(\), std::stol\(\), std::stoll\(\)|" +
            r"is well documented, e\.g\. in" +
        r")\s\[)\d{1,2}(\])",
        r"\1 \3", textdata)

    # 17-10[17], 19-10[18]
    # open-std.org, site holding a number of web pages for groups producing open
    # standards, 2017
    textdata = re.sub(r"((" +
            r"open-std\.org|" +
            r"C\+\+ Standard Core Language Active Issues, Revision 96|" +
            r"C\+\+ Standard Core Language Defect Reports and Accepted Issues, Revision 96" +
        r")\s\[)\d{1,2}(\])",
        r"\1 \3", textdata)

    return textdata
