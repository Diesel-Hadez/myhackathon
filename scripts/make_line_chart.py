import matplotlib.pyplot as plt
import pandas as pd
from math import pi

def load_from_file(filename):
    ret = []
    with open(filename, 'r') as f:
        line = f.readline()
        while line != '':
            ret.append([])
            ret[-1].append(float(line.strip()))
            line = f.readline()

def make_line_chart(lst,title="", filename=""):
    plt.title(title)
    plt.plot([_ for _ in range(len(lst))], lst)
    plt.show()
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
