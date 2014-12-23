#!/usr/bin/env python

# Author: Sawood Alam <ibnesayeed@gmail.com>
#
# This scripts generates multiple profiles from the same collect with varying configurations and benchmarks them.

import os
import sys
import json
import time

from profile import Profile
from cdx_profiler import CDXProfiler

def write_json(jsonstr="{}", filepath="profile.json"):
    """Save JSON on local filesystem."""
    print("Writing output to " + filepath)
    f = open(filepath, "w")
    f.write(jsonstr)
    f.close()

def build_profile(host, path):
    print("Profiling UKWA 2000 with Host: {0}, Path: {1}".format(host, path))
    profile_id = "ukwa-2000-host-{0}-path-{1}".format(host, path)
    profiling_start = time.time()
    p = Profile(name="UKWA 2000 Hosts {0} Paths {1}".format(host, path),
                description="UK Web Archive 2000 collection profile with maximum {0} host and {1} path secgment(s).".format(host, path),
                homepage="http://www.webarchive.org.uk/ukwa/",
                accesspoint="http://www.webarchive.org.uk/wayback/",
                memento_compliance="https://oduwsdl.github.io/terms/mementosupport#native",
                timegate="http://www.webarchive.org.uk/wayback/archive/",
                timemap="http://www.webarchive.org.uk/wayback/archive/timemap/link/",
                established="2004",
                profile_updated=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                mechanism="https://oduwsdl.github.io/terms/mechanism#cdx")
    cp = CDXProfiler(max_host_segments=host,
                     max_path_segments=path,
                     global_stats=True)
    cp.process_cdxes(sys.argv[1:])
    cdx_processing_done = time.time()
    cp.calculate_stats()
    stats_calculation_done = time.time()
    p.stats = cp.stats
    jsonstr = p.to_json()
    opf = "profile-{0}.json".format(profile_id)
    opfpath = os.path.join(scriptdir, "benchmark", opf)
    write_json(jsonstr, filepath=opfpath)
    profiling_done = time.time()
    bm = {
        "profile": opf,
        "collection": "ukwa-2000",
        "max_host": host,
        "max_path": path,
        "cdx_size": cdx_size,
        "cdx_lines_total": cp.total_lines,
        "cdx_lines_skipped": cp.skipped_lines,
        "profile_size": os.path.getsize(opfpath),
        "suburi_keys": len(p.stats["suburi"]),
        "time_keys": len(p.stats["time"]),
        "mediatype_keys": len(p.stats["mediatype"]),
        "language_keys": len(p.stats["language"]),
        "cdx_processing_time": cdx_processing_done - profiling_start,
        "stats_calculation_time": stats_calculation_done - cdx_processing_done,
        "profiling_time": profiling_done - profiling_start
    }
    all_bms[profile_id] = bm
    jsonstr = json.dumps(bm, indent=4, separators=(",", ": "))
    opf = "bm-{0}.json".format(profile_id)
    opfpath = os.path.join(scriptdir, "benchmark", opf)
    write_json(jsonstr, filepath=opfpath)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide path(s) to CDX file(s) as command line argument(s)")
        sys.exit(0)
    benchmarking_start = time.time()
    scriptdir = os.path.dirname(os.path.abspath(__file__))
    cdx_size = sum(os.path.getsize(f) for f in sys.argv[1:])
    all_bms = {"collection": "ukwa-2000"}
    path = 0
    for host in [1, 2, 3, 4, 5, "all"]:
        build_profile(host, path)
    for path in [1, 2, 3, 4, 5, "all"]:
        build_profile(host, path)
    benchmarking_done = time.time()
    all_bms["benchmarking_time"] = benchmarking_done - benchmarking_start
    jsonstr = json.dumps(all_bms, indent=4, separators=(",", ": "))
    opfpath = os.path.join(scriptdir, "benchmark", "bm-ukwa-2000.json")
    write_json(jsonstr, filepath=opfpath)
    print("All Done!")
