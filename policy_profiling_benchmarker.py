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
from key_generator import KeyGenerator

def write_json(jsonstr="{}", filepath="profile.json"):
    """Save JSON on local filesystem."""
    print("Writing output to " + filepath)
    f = open(filepath, "w")
    f.write(jsonstr)
    f.close()

def file_len(fname):
    i = 0
    with open(fname) as f:
        for i, _ in enumerate(f, 1):
            pass
    return i

def build_profile(policy):
    print("Profiling {0} with Policy: {1}".format(collection, policy))
    profile_id = "{0}-{1}".format(col_id, policy)
    profiling_start = time.time()
    p = Profile(name="{0} Policy {1}".format(collection, policy),
                description="{0} collection profile with policy {1}.".format(collection, policy),
                homepage="http://www.webarchive.org.uk/ukwa/",
                accesspoint="http://www.webarchive.org.uk/wayback/",
                memento_compliance="https://oduwsdl.github.io/terms/mementosupport#native",
                timegate="http://www.webarchive.org.uk/wayback/archive/",
                timemap="http://www.webarchive.org.uk/wayback/archive/timemap/link/",
                established="2004",
                profile_updated=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                mechanism="https://oduwsdl.github.io/terms/mechanism#cdx",
                policy="https://oduwsdl.github.io/terms/policy#{0}".format(policy))
    opkfn = "intermediate-{0}.keys".format(profile_id)
    opkfpath = os.path.join(bmdir, opkfn)
    opkf = open(opkfpath, "w")
    kg = KeyGenerator(policy)
    kg.generate_keys_from_files(sys.argv[1:], opkf)
    opkf.close()
    key_generation_done = time.time()
    oppfn = "profile-{0}.cdxj".format(profile_id)
    oppfpath = os.path.join(bmdir, oppfn)
    oppf = open(oppfpath, "w")
    pabout = json.dumps(p.about, sort_keys=True)
    oppf.write("@about " + pabout + "\n")
    oppf.close()
    os.system('LC_ALL=C sort ' + opkfpath + ' | uniq -c | awk \'{ print $2 " {\\"frequency\\": "$1", \\"spread\\": 1}" }\' >> ' + oppfpath)
    profile_generation_done = time.time()
    os.system('gzip -c ' + oppfpath + ' > ' + oppfpath + '.gz')
    profile_compression_done = time.time()
    bm = {
        "profile": oppfn,
        "collection": col_id,
        "policy": policy,
        "cdx_size": cdx_size,
        "extract_size": extract_size,
        "profile_size": os.path.getsize(oppfpath),
        "profile_size_compressed": os.path.getsize(oppfpath + ".gz"),
        "urir_count": urir_count,
        "urim_count": urim_count,
        "keys_count": file_len(oppfpath),
        "key_generation_time": key_generation_done - profiling_start,
        "profile_generation_time": profile_generation_done - key_generation_done,
        "profile_compression_time": profile_compression_done - profile_generation_done,
        "profiling_time": profile_generation_done - profiling_start
    }
    all_bms["bms"][policy] = bm
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
    bmdir = os.path.join(scriptdir, "policybm", col_id)
    if not os.path.exists(bmdir):
        os.makedirs(bmdir)
    extract_size = sum(os.path.getsize(f) for f in sys.argv[1:])
    cdx_size = sum(os.path.getsize(f.replace(".urir", ".cdx")) for f in sys.argv[1:])
    urir_count = sum(file_len(f) for f in sys.argv[1:])
    urim_count = sum(file_len(f.replace(".urir", ".cdx")) for f in sys.argv[1:])
    all_bms = {"about": {"id": col_id, "name": collection}, "bms": {}}
    policies = "H1P0 H2P0 H2P1 H2P2 H3P0 H3P1 H3P2 H3P3 H4P0 H5P0 HxP0 HxP1 HxP2 HxP3 HxP4 HxP5 HxPx DDom DSub DPth DQry DIni".split()
    for policy in policies:
        build_profile(policy)
    benchmarking_done = time.time()
    all_bms["about"]["benchmarking_time"] = benchmarking_done - benchmarking_start
    jsonstr = json.dumps(all_bms, sort_keys=True, indent=4, separators=(",", ": "))
    opfpath = os.path.join(bmdir, "bm-{0}.json".format(col_id))
    write_json(jsonstr, filepath=opfpath)
    print("All Done! (Time: {0} minutes)\n".format(int(all_bms["about"]["benchmarking_time"]/60)))
