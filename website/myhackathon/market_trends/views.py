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



# Should probably put this in a separate file
# Or import from root

# Create your views here.
def index(request):
    return render(request, 'index.html', context={})

import json
from django.http import JsonResponse
def radar_chart(request):
    lst = [(name, float(data.strip())) for name, data in json.loads(request.GET['data']).items()]
    data = make_radar_chart(lst)
    return HttpResponse(data, "image/png")
