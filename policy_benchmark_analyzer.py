#!/usr/bin/env python

# Author: Sawood Alam <ibnesayeed@gmail.com>
#
# This scripts analyzes benchmarks and creates summary files to generate plots.

import os
import sys
import json
from collections import OrderedDict

def process_benchmarks(benchmarks):
    """Accepts a list of JSON benchmark file names/paths and creates CSV summary from them."""
    print("Benchmarking started...")
    for bm in benchmarks:
        print("Benchmarking: " + bm)
        f = open(bm, "r")
        data = json.load(f)
        f.close()
        policies = ["H1P0",
                    "H2P0",
                    "H2P1",
                    "H2P2",
                    "DDom",
                    "H3P0",
                    "DSub",
                    "H4P0",
                    "H5P0",
                    "HxP0",
                    "DPth",
                    "DQry",
                    "DIni",
                    "H3P1",
                    "HxP1",
                    "H3P2",
                    "H3P3",
                    "HxP2",
                    "HxP3",
                    "HxP4",
                    "HxP5",
                    "HxPx"]
        flds = ["policy",
                "keys_count",
                "profile_size",
                "profile_size_compressed",
                "key_generation_time",
                "profile_generation_time",
                "profiling_time",
                "collection",
                "cdx_size",
                "extract_size",
                "urim_count",
                "urir_count"]
        opstr = ", ".join(flds)
        for p in policies:
            opstr += "\n" + ", ".join([str(data["bms"][p][i]) for i in flds])
        print(opstr)
        bmdir = os.path.dirname(os.path.abspath(bm))
        summary = os.path.join(bmdir, "summary-{0}.csv".format(data["about"]["id"]))
        f = open(summary, "w")
        f.write(opstr)
        f.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide path to benchmark JSON file(s) as command line argument.")
        sys.exit(0)
    print("Analyzing benchmarks...")
    process_benchmarks(sys.argv[1:])
