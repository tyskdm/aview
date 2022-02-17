"""
create_json.py
"""
import re
from . import fsm

# DATA STRUCTURE
# [
#     "A1-1-1": {
#         "section" = ["", ""]
#         "class": [],
#         "rule": "text",
#         "note": ["", "",...],       # MISRAへの参照もここに含む
#         "rationale": [],
#         "exception": [],
#         "example": [],
#         "see also": [],
#     }
# ]

class Section(fsm.StateMachine):

    def __init__(self) -> None:
        super().__init__(name="Section")
        self.section = ["", "", ""]

    def on_entry(self, e=None):
        if e:
            # set section name
            line = e[0]
            data = e[1]

            match = re.match(r"^(#{1,3}) (\d.+)$", line)
            if match:
                level = len(match.group(1)) - 1
                self.section[level] = match.group(2)

        return super().on_entry(e + [self.section])

    def on_event(self, e):
        # set section name
        line = e[0]
        data = e[1]
        match = re.match(r"^#{1,3}\s+\d{1,2}(\.\d{1,2})*\s.+$", line)

        if match:
            next = (self, e)
        else:
            next = super().on_event(e + [self.section])

        return next


class Rule(fsm.State):

    def __init__(self) -> None:
        super().__init__(name="Rule")

        self.inside_rule = False
        self.rule_data = None
        self.prop_name = None


    def on_entry(self, e=None):
        self.inside_rule = False

        if e:
            # set section name
            line = e[0]
            data = e[1]

            # #### Rule A2-8-1 (required, implementation, automated)<br>The character \ shall
            # not occur as a last character of a C++ comment.

            match = re.match(r"^#{4} Rule ([MA]?\d{1,2}[-–]\d{1,2}[-–]\d{1,2})\s*" +
                             r"\((.+)\)<br>(.*)$", line)
            if match:
                self.rule_data = {
                    "Section": e[-1][:],
                    "Class": [x.strip() for x in match.group(2).split(',')],
                    "Rule": match.group(3)
                }
                data[match.group(1)] = self.rule_data
                self.prop_name = "Note"
                self.inside_rule = True

        return super().on_entry(e)


    def on_event(self, e):
        # set section name
        line = e[0]
        data = e[1]

        # #### Rule A2-8-1 (required, implementation, automated)<br>The character \ shall
        # not occur as a last character of a C++ comment.

        match = re.match(r"^#{4} Rule ([MA]?\d{1,2}[-–]\d{1,2}[-–]\d{1,2})\s*" +
                            r"\((.+)\)<br>(.*)$", line)
        if match:
            next = (self, e)    # Reopen

        else:
            next = self
            if self.inside_rule:

                match = re.match(
                    r"^#{5} (Rationale|Exception|Example|See also)$", line)

                if match:
                    self.prop_name = match.group(1)
                    self.rule_data[self.prop_name] = []

                elif line != '':
                    if self.prop_name not in self.rule_data:
                        self.rule_data[self.prop_name] = []

                    self.rule_data[self.prop_name].append(line)

        return next


def create_object(textdata):

    m = fsm.StateMachine(name = "root fsm").add_state(
        Section().add_state(
            Rule()
        )
    )

    lines = textdata.split('\n')
    data = {}

    m.start(["", data])

    for line in lines:
        m.process_event([line, data])

    m.stop()

    return data
