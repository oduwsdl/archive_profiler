#!/usr/bin/env python

# Author: Sawood Alam <ibnesayeed@gmail.com>
#
# This scripts generates multiple profiles from the same collection with varying configurations and benchmarks them.

import os
import sys
import gzip
import json
import time
import re

from profile import Profile
from cdx_extract_profiler import CDXExtractProfiler

def write_json(jsonstr="{}", filepath="profile.json", compress=False):
    """Save JSON on local filesystem."""
    print("Writing output to " + filepath)
    f = open(filepath, "w")
    f.write(jsonstr)
    f.close()
    if compress:
        with open(filepath, "rb") as f_in:
            f_out = gzip.open(filepath + ".gz", "wb")
            while True:
                block = f_in.read(1048576)
                if block == "":
                    break
                f_out.write(block)
            f_out.close()
        #zf = gzip.open(filepath + ".gz", "wb")
        #zf.write(jsonstr)
        #zf.close()

def build_profile(host, path):
    print("Profiling {0} with Host: {1}, Path: {2}".format(collection, host, path))
    bm_id = "H{0}P{1}".format(host, path)
    profile_id = "{0}-{1}".format(col_id, bm_id)
    profiling_start = time.time()
    p = Profile(name="{0} Hosts {1} Paths {2}".format(collection, host, path),
                description="{0} collection profile with maximum {1} host and {2} path secgment(s).".format(collection, host, path),
                homepage="http://www.webarchive.org.uk/ukwa/",
                accesspoint="http://www.webarchive.org.uk/wayback/",
                memento_compliance="https://oduwsdl.github.io/terms/mementosupport#native",
                timegate="http://www.webarchive.org.uk/wayback/archive/",
                timemap="http://www.webarchive.org.uk/wayback/archive/timemap/link/",
                established="2004",
                profile_updated=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                mechanism="https://oduwsdl.github.io/terms/mechanism#cdx")
    cp = CDXExtractProfiler(max_host_segments=host,
                            max_path_segments=path,
                            global_stats=True)
    cp.process_cdx_extracts(sys.argv[1:])
    cdx_processing_done = time.time()
    cp.calculate_stats()
    stats_calculation_done = time.time()
    p.stats = cp.stats
    jsonstr = p.to_json()
    opf = "profile-{0}.json".format(profile_id)
    opfpath = os.path.join(bmdir, opf)
    write_json(jsonstr, filepath=opfpath, compress=True)
    profiling_done = time.time()
    bm = {
        "profile": opf,
        "collection": col_id,
        "max_host": host,
        "max_path": path,
        "cdx_size": cdx_size,
        "extract_size": extract_size,
        "profile_size": os.path.getsize(opfpath),
        "profile_size_compressed": os.path.getsize(opfpath + ".gz"),
        "urir_count": p.stats["urir"],
        "urim_count": p.stats["urim"]["total"],
        "suburi_keys": len(p.stats["suburi"]),
        "time_keys": len(p.stats["time"]),
        "mediatype_keys": len(p.stats["mediatype"]),
        "language_keys": len(p.stats["language"]),
        "cdx_processing_time": cdx_processing_done - profiling_start,
        "stats_calculation_time": stats_calculation_done - cdx_processing_done,
        "profiling_time": profiling_done - profiling_start
    }
    all_bms["bms"][bm_id] = bm
    jsonstr = json.dumps(bm, sort_keys=True, indent=4, separators=(",", ": "))
    opf = "bm-{0}.json".format(profile_id)
    opfpath = os.path.join(bmdir, opf)
    write_json(jsonstr, filepath=opfpath)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide path(s) to CDX Extraxt file(s) as command line argument(s).")
        sys.exit(0)
    print("\n{0} => Running: {1}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"), sys.argv))
    benchmarking_start = time.time()
    collection = os.getenv("COLLECTION", "Test CDX Extraxt")
    col_id = re.sub("\W+", "-", collection.lower())
    scriptdir = os.path.dirname(os.path.abspath(__file__))
    bmdir = os.path.join(scriptdir, "extractbm", col_id)
    if not os.path.exists(bmdir):
        os.makedirs(bmdir)
    extract_size = sum(os.path.getsize(f) for f in sys.argv[1:])
    cdx_size = sum(os.path.getsize(f.replace(".curi", ".cdx")) for f in sys.argv[1:])
    all_bms = {"about": {"id": col_id, "name": collection}, "bms": {}}
    host_path_pairs = [(1, 0), (2, 0), (2, 1), (2, 2), (3, 0), (3, 1), (3, 2), (3, 3), (4, 0), (5, 0), ("x", 0), ("x", 1), ("x", 2), ("x", 3), ("x", 4), ("x", 5), ("x", "x")]
    for host, path in host_path_pairs:
        build_profile(host, path)
    benchmarking_done = time.time()
    all_bms["about"]["benchmarking_time"] = benchmarking_done - benchmarking_start
    jsonstr = json.dumps(all_bms, sort_keys=True, indent=4, separators=(",", ": "))
    opfpath = os.path.join(bmdir, "bm-{0}.json".format(col_id))
    write_json(jsonstr, filepath=opfpath)
    print("All Done! (Time: {0} minutes)\n".format(int(all_bms["about"]["benchmarking_time"]/60)))
