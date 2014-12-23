#!/usr/bin/env python

# Author: Sawood Alam <ibnesayeed@gmail.com>
#
# This scripts instantiate a Profile object, (optionally populates it from a JSON profile,) updates it using different profilres, and serializes it in JSON.

import os
import sys
import pprint
import json
import time
import requests
import ConfigParser

from profile import Profile
from cdx_profiler import CDXProfiler

def print_help():
    """Print help text."""
    print("\nTo profile a CDX archive:")
    print("  Single CDX file    :    main.py abc.cdx")
    print("  Multiple CDX files :    main.py abc.cdx def.cdx ...")
    print("  Multiple CDX files :    main.py *.cdx abc/*.cdx ...\n")

def write_json(jsonstr="{}", filepath="profile.json"):
    """Save JSON profile on local filesystem."""
    print("Writing output to " + filepath)
    f = open(filepath, "w")
    f.write(jsonstr)
    f.close()

def post_gist(jsonstr="{}", filename="profile.json"):
    """Post JSON profile to GitHub as a Gist."""
    gist = {
        "description": "An archive profile created on "+time.strftime("%Y-%m-%d at %H:%M:%S")+".",
        "public": True,
        "files": {
            filename: {
                "content": jsonstr
            }
        }
    }
    req = requests.post(config.get("github", "endpoint"),
                        data=json.dumps(gist),
                        auth=(config.get("github", "user"), config.get("github", "token")))
    if req.status_code == 201:
        print("Writing to GitHub: " + req.json()["html_url"])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)
    scriptdir = os.path.dirname(os.path.abspath(__file__))
    config = ConfigParser.ConfigParser()
    config.read(os.path.join(scriptdir, "config.ini"))
    p = Profile(name=config.get("archive", "name"),
                description=config.get("archive", "description"),
                homepage=config.get("archive", "homepage"),
                accesspoint=config.get("archive", "accesspoint"),
                memento_compliance=config.get("archive", "memento_compliance"),
                timegate=config.get("archive", "timegate"),
                timemap=config.get("archive", "timemap"),
                established=config.get("archive", "established"),
                profile_updated=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                mechanism="https://oduwsdl.github.io/terms/mechanism#cdx")
    cp = CDXProfiler(max_host_segments=config.get("profile", "max_host_segments"),
                     max_path_segments=config.get("profile", "max_path_segments"),
                     global_stats=config.getboolean("profile", "generate_global_stats"))
    cp.process_cdxes(sys.argv[1:])
    cp.calculate_stats()
    p.stats = cp.stats
    if config.getboolean("profile", "generate_key_stats"):
        p.count_keys()
    jsonstr = p.to_json()
    opf = "profile-"+time.strftime("%Y%m%d-%H%M%S")+".json"
    if config.getboolean("output", "write_to_file"):
        write_json(jsonstr, filepath=os.path.join(scriptdir, "json", opf))
    else:
        print(jsonstr)
    if config.getboolean("output", "write_to_github"):
        post_gist(jsonstr, filename=opf)
