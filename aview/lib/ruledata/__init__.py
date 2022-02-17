r"""!

subcommand **dump**\n

"""
import re

from .create_json import create_object
from .format_text import format_2008
from . import pdftotext

def get_misra_data(filename):

    textdata = pdftotext.run(filename).decode()

    m = re.search(r"^(License terms: .+(\n.+)+)$", textdata, flags=re.MULTILINE)
    LicenseTerms = m.group(1)
    LicenseTerms = LicenseTerms.split('\n')
    for i in range(len(LicenseTerms)):
        while not LicenseTerms[i].endswith('.'):
            LicenseTerms[i] += ' ' + LicenseTerms[i+1]
            del LicenseTerms[i+1]

        if i == len(LicenseTerms) - 1:
            break

    print("===== [ " + filename + " ]")
    print("\n".join(LicenseTerms))
    print("=====\n")

    return create_object(format_2008(textdata))

