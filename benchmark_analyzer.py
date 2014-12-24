#!/usr/bin/env python

# Author: Sawood Alam <ibnesayeed@gmail.com>
#
# This scripts analyzes benchmarks and creates summary files to generate plots.

import os
import sys
import json
from collections import OrderedDict

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide path to benchmark JSON file as command line argument.")
        sys.exit(0)
    print("Analyzing benchmarks...")
    f = open(sys.argv[1], "r")
    data = json.load(f)
    f.close()
    bms = OrderedDict(sorted(data["bms"].items()))
    opstr = ", ".join(["profile_id", "profiling_time", "profile_size", "suburi_keys"])
    for k, v in bms.iteritems():
        opstr += "\n" + ", ".join([k[10:], str(v["profiling_time"]), str(v["profile_size"]), str(v["suburi_keys"])])
    print(opstr)
    f = open("benchmark/summary.csv", "w")
    f.write(opstr)
    f.close()
