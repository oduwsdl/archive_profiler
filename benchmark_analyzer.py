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
        bms = OrderedDict(sorted(data["bms"].items()))
        flds = ["profile_id",
                "suburi_keys",
                "mediatype_keys",
                "time_keys",
                "language_keys",
                "profile_size",
                "profile_size_compressed",
                "cdx_processing_time",
                "stats_calculation_time",
                "profiling_time",
                "collection",
                "cdx_size",
                "cdx_lines_total",
                "cdx_lines_skipped",
                "urim_count",
                "urir_count"]
        opstr = ", ".join(flds)
        for k, v in bms.iteritems():
            v["profile_id"] = k
            opstr += "\n" + ", ".join([str(v[i]) for i in flds])
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
