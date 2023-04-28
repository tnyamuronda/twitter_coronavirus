#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict
import matplotlib.pyplot as plt
# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# print the count values
#items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)
#for k,v in items:
#   print(k,':',v)
items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]))[:10]

# create a bar graph of the results
keys = [item[0] for item in items]
values = [item[1] for item in items]
plt.bar(keys, values)

# set the title and labels of the graph
plt.title(args.key + ' Counts')
plt.xlabel('country')
plt.ylabel('Values')

# save the graph as a png file
output_path = 'Country' + '_' + args.key + '.png'
plt.savefig(output_path)
