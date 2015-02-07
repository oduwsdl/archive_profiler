#!/usr/bin/env python

# Author: Sawood Alam <ibnesayeed@gmail.com>
#
# This scripts generates Sub-URIs from extracted URI-Rs based on various profile configurations.

import os
import sys
import time

from surt import surt
from suburi_generator import generate_suburis

def generate_all_suburis(host, path):
    print("Generating Sub-URIs of {0} with Host: {1}, Path: {2}".format(collection, host, path))
    filename = "{0}-H{1}P{2}.suburi".format(collection, host, path)
    opf = open(os.path.join(opdir, filename), "w")
    for extr in sys.argv[1:]:
        with open(extr) as f:
            for line in f:
                count, entry = line.split()
                try:
                    opf.write("\n".join(generate_suburis(surt(entry), max_host_segments=host, max_path_segments=path)) + "\n")
                except:
                    print("Something went wrong while processing " + line)
    opf.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide path(s) to CDX Extraxt file(s) as command line argument(s).")
        sys.exit(0)
    print("\n{0} => Running: {1}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"), sys.argv))
    suburidir = os.getenv("SUBURIDIR", "/tmp/suburis")
    collection = os.getenv("COLLECTION", "0000")
    opdir = os.path.join(suburidir, collection)
    if not os.path.exists(opdir):
        os.makedirs(opdir)
    host_path_pairs = [(1, 0), (2, 0), (2, 1), (2, 2), (3, 0), (3, 1), (3, 2), (3, 3), (4, 0), (5, 0), ("x", 0), ("x", 1), ("x", 2), ("x", 3), ("x", 4), ("x", 5), ("x", "x")]
    for host, path in host_path_pairs:
        gen_start = time.time()
        generate_all_suburis(host, path)
        gen_end = time.time()
        print("It took {0} minutes.".format(round((gen_end - gen_start)/60, 2)))
    print("All Done!")
