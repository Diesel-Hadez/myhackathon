import enum
import uuid

class NodeType(enum.Enum):
    SKILL = 1
    AND = 2
    OR = 3

class Node:
    def __init__(self, label, type=NodeType.SKILL, fulfilled=False):
        self.label = label
        self.type = type
        self.uuid = uuid.uuid4().int
        self.parents = []
        self.fulfilled = False
    def add_parent(self, node):
        if node not in self.parents:
            self.parents.append(node)
    def set_fulfilled(self):
        self.fulfilled = True
    def __repr__(self):
        return self.label

def parents_till_needed(node):
    if node.fulfilled:
        return []

    ret = []
    if node.type == NodeType.AND:
        for parent in node.parents:
            if not parent.fulfilled:
                ret.append(parents_till_needed(parent))
    if node.type == NodeType.OR:
        for parent in node.parents:
            if parent.fulfilled:
                return []
        for parent in node.parents:
            ret += parents_till_needed(parent)
    if node.type == NodeType.SKILL:
        if len(node.parents) == 0:
            return [node]
        for parent in node.parents:
            if not parent.fulfilled:
                ret += parents_till_needed(parent)
    return ret


def parents_till_fulfilled(node, miu=False):
    if node.fulfilled:
        return []
    ret = []

    if node.type == NodeType.SKILL:
        ret.append(node)

    if len(node.parents) == 0:
        return ret

    for parent in node.parents:
        if parent.type == NodeType.AND and not parent.fulfilled:
            ret += parents_till_fulfilled(parent, True)
        elif parent.type == NodeType.OR:
            ret.append([])
            for parent2 in node.parents:
                # The difference is this one appends a list to
                # account for the different possibilities
                if not parent2.fulfilled:
                    ret[-1] += (parents_till_fulfilled(parent2, True))
                else:
                    ret.pop()
                    break
        elif parent.type == NodeType.SKILL and not parent.fulfilled and miu:
            ret.append(parent)
    return ret

def fulfill_skills(my_skills, skilltree):
    for x in skilltree:
        if x.label in my_skills:
            x.set_fulfilled()
def more_needed_for_job(my_skills, skill_wanted, skilltree):
    fulfill_skills(my_skills, skilltree)
    return parents_till_fulfilled(skill_wanted)

def demo():
    web_dev = [Node("JS"), Node("HTML"), Node("Phoenix"), Node("NodeJS"), Node("php")]

    and_1 = Node("AND_1", NodeType.AND)
    or_1 = Node("OR_1", NodeType.OR)

    and_1.add_parent(web_dev[0])
    and_1.add_parent(web_dev[1])
    and_1.add_parent(or_1)

    or_1.add_parent(web_dev[2])
    or_1.add_parent(web_dev[3])
    or_1.add_parent(web_dev[4])

    # After learning JS
    web_dev[0].set_fulfilled()

    # After learning php
    web_dev[4].set_fulfilled()

    final= Node("web_dev", NodeType.AND)
    final.add_parent(and_1)

    my_list = parents_till_needed(final)[0]
    print(my_list)
    ret = ""
    for x in range(len(my_list)):
        ret += "("
        for y in range(len(my_list[x])):
            ret += str(my_list[x][y]) + " or "
        ret = ret[:-4]
        ret += ")"
        ret += " and "
    ret = ret[:-5]
    print(ret)

    for i in my_list:
        print(i)

demo()