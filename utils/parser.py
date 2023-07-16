from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

class RemindmeParser(NodeVisitor):
    UNIT_TO_SECONDS = {
        "s": 1,
        "m": 60,
        "h": 60 * 60,
        "d": 60 * 60 * 24,
        "w": 60 * 60 * 24 * 7,
    }

    def __init__(self, grammar):
        self.grammar = Grammar(grammar)

    def visit_rm(self, node, visited_children):
        return self.append_children(node, visited_children)

    def visit_msg(self, node, _):
        return {'msg': node.text}

    def visit_method(self, node, visited_children):
        return self.append_children(node, visited_children)

    def visit_all(self, node, _):
        return {'all': True}

    def visit_HMS(self, node, visited_children):
        return self.append_children(node, visited_children)

    def visit_Date(self, node, visited_children):
        return self.append_children(node, visited_children)

    def visit_Time(self, node, visited_children):
        return self.append_children(node, visited_children)

    def visit_DateTime(self, node, visited_children):
        return self.append_children(node, visited_children)

    def visit_DMY(self, node, visited_children):
        return self.append_children(node, visited_children)

    def visit_YMD(self, node, visited_children):
        return self.append_children(node, visited_children)

    def append_children(self, _, visited_children):
        output = {}
        for child in visited_children:
            if child is not None and (child[0] is not None if isinstance(child, list) else True):
                output.update(child[0] if isinstance(child, list) else child)
        return output

    def visit_RemindTime(self, _, visited_children):
        output = {}
        for child in visited_children:
            output.update({'remind_time': child})
        return output

    def visit_DateSep(self, _, _children):
        return None

    def visit_Year(self, node, _):
        return {'year': int(node.text)}

    def visit_Year4(self, node, _):
        return {'year': int(node.text)}

    def visit_Month(self, node, _):
        return {'month': int(node.text)}

    def visit_Day(self, node, _):
        return {'day': int(node.text)}

    def visit_Hour(self, node, _):
        return {'hour': int(node.text)}

    def visit_Minute(self, node, _):
        return {'minute': int(node.text)}

    def visit_Second(self, node, _):
        return {'second': int(node.text)}

    def visit_Duration(self, node, _):
        matches = node.match
        duration = int(matches.group(1))
        unit = matches.group(2)
        return {'duration_seconds': duration * self.UNIT_TO_SECONDS[unit]}

    def generic_visit(self, node, visited_children):
        return visited_children or node
