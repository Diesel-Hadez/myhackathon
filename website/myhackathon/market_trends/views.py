from django.shortcuts import render
from django.http import HttpResponse

import matplotlib.pyplot as plt
import pandas as pd
from math import pi


def make_radar_chart(lst, filename=""):
    categories = []
    values = []
    for i in lst:
        if i[0] not in categories:
            categories.append(i[0])
            values.append(0)
        index = categories.index(i[0])
        values[index] += i[1]
    # Weird quirk of matplotlib is the last one should be
    # a duplicate of the first one
    values += values[:1]
    n = len(categories)
    angles = [_ / float(n) * 2 * pi for _ in range(n)]
    angles += angles[:1]

    plt.polar(angles, values)
    plt.xticks(angles[:-1], categories)

    if filename:
        plt.savefig(filename)
        plt.clf()
    else:
        import io
        ret = io.BytesIO()
        plt.savefig(ret, format='png')
        plt.clf()
        ret.seek(0)
        return ret.read()


def resume_creator(profile):
    """
    Create a short user description from template

    Args:
        profile: A list containg user's name, list of expertise and list of work experience
    Returns:
        A string with the profile description
    """
    name, expertise, work_exp = profile
    expertise = ", ".join(expertise)
    work_exp = ", ".join(work_exp)
    template = "My name is {}. My expertise are in {}. My work experience include {}"
    return template.format(name, expertise, work_exp)


def my_resume(request):
    name = request.GET['name']
    work_exp = request.GET['work_exp']
    expertise = request.GET['expertise']

    # Can do it as a list too but for the presentation I need to get it done
    return HttpResponse(resume_creator((name, [expertise], [work_exp])))


# Should probably put this in a separate file
# Or import from root


# Create your views here.
def index(request):
    return render(request, 'index.html', context={})


import json
from django.http import JsonResponse


def radar_chart(request):
    lst = [(name, float(data.strip()))
           for name, data in json.loads(request.GET['data']).items()]
    data = make_radar_chart(lst)
    return HttpResponse(data, "image/png")


def make_line_chart(lst, title="", filename=""):
    plt.title(title)
    plt.plot([_ for _ in range(len(lst))], lst)
    if filename:
        plt.savefig(filename)
        plt.clf()
    else:
        import io
        ret = io.BytesIO()
        plt.savefig(ret, format='png')
        plt.clf()
        ret.seek(0)
        return ret.read()


def line_chart(request):
    lst = request.GET.getlist('data[]')
    lst = [float(x.strip()) for x in lst]
    title = request.GET['title']
    data = make_line_chart(lst, title)
    return HttpResponse(data, "image/png")


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
            ret += parents_till_fulfilled(parent)
        elif parent.type == NodeType.OR:
            ret.append([])
            for parent in node.parents:
                # The difference is this one appends a list to
                # account for the different possibilities
                if not parent.fulfilled:
                    ret[-1].append(parents_till_fulfilled(parent, True))
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


def job_parse(request):
    web_dev = [
        Node("JS"),
        Node("HTML"),
        Node("Phoenix"),
        Node("NodeJS"),
        Node("php")
    ]
    lst = request.GET.getlist('data[]')
    for i in lst:
        for x in web_dev:
            if x.label == i:
                x.set_fulfilled()

    and_1 = Node("AND_1 (Webdev)", NodeType.AND)
    or_1 = Node("OR_1", NodeType.OR)

    and_1.add_parent(web_dev[0])
    and_1.add_parent(web_dev[1])
    and_1.add_parent(or_1)

    or_1.add_parent(web_dev[2])
    or_1.add_parent(web_dev[3])
    or_1.add_parent(web_dev[4])
    final = Node("webdev", NodeType.AND)
    final.add_parent(and_1)
    my_list = parents_till_needed(final)[0]
    ret = ""
    for x in range(len(my_list)):
        if (len(my_list[x]) > 1):
            ret += "("
        for y in range(len(my_list[x])):
            ret += str(my_list[x][y]) + " or "
        ret = ret[:-4]
        if (len(my_list[x]) > 1):
            ret += ")"
        ret += " and "
    ret = ret[:-5]
    return HttpResponse(ret)


def txt_to_list(keyword, fname):
    """
    Return text in a .txt file as a string
    """
    with open(fname, 'r') as f:
        ret_str = f.read()
    return ret_str


def keywords_in_str(keywords_lst, text):
    """
    Finds all keywords in a text string
    
    Args:
        keywords_lst: A list of keywords to search in text
        text: A string
    Returns:
        A list of capitalized strings for all keywords found in text.

    References:
    https://medium.com/quantrium-tech/extracting-words-from-a-string-in-python-using-regex-dac4b385c1b8
    https://docs.python.org/3/library/re.html
    https://docs.python.org/3/library/string.html#string.capwords
    """
    import re, string
    keywords = '|'.join(keywords_lst)
    found_lst = re.findall(keywords, text, flags=re.IGNORECASE)
    found_lst = set(map(string.capwords, found_lst))
    return list(found_lst)

def keywword_search(request):
    resume = request.GET['resume']
    # Can easily be from a file too using
    # the txt_to_list function
    # Here I use hard-coded samples
    keywords = keywords_in_str(["Big Data", "Blockchain"], resume)
    if len(keywords) == 0:
        return HttpResponse("No keywords!")
    return HttpResponse("Found keywords: " + ','.join(keywords))
