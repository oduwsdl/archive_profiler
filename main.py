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

def write_json(jsonstr="{}"):
    """Save JSON profile on local filesystem."""
    scriptdir = os.path.dirname(os.path.abspath(__file__))
    opf = os.path.join(scriptdir, 'json', "profile-"+time.strftime("%Y%m%d-%H%M%S")+".json")
    print("Writing output to " + opf)
    f = open(opf, 'w')
    f.write(jsonstr)
    f.close()

def post_gist(jsonstr="{}"):
    """Post JSON profile to GitHub as a Gist."""
    gist = {
        "description": "An archive profile created on "+time.strftime("%Y-%m-%d at %H:%M:%S")+".",
        "public": True,
        "files": {
            "profile-"+time.strftime("%Y%m%d-%H%M%S")+".json": {
                "content": jsonstr
            }
        }
    }
    req = requests.post(config.get("github", "endpoint"),
                        data=json.dumps(gist),
                        auth=(config.get("github", "user"), config.get("github", "token")))
    if req.status_code == 201:
        print("Writing to GitHub: " + req.json()["html_url"])

def generate_key_stats(profile):
    """Save key statistics in JSON format on local filesystem."""
    scriptdir = os.path.dirname(os.path.abspath(__file__))
    opf = os.path.join(scriptdir, 'json', "keystats-"+time.strftime("%Y%m%d-%H%M%S")+".json")
    f = open(opf, 'w')
    json.dump(profile.count_keys(), f, sort_keys=True, indent=4, separators=(',', ': '))
    f.close()

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
                     max_path_segments=config.get("profile", "max_path_segments"))
    cp.process_cdxes(sys.argv[1:])
    cp.calculate_stats()
    p.stats = cp.stats
    p.count_keys()
    jsonstr = p.to_json()
    write_json(jsonstr)
    post_gist(jsonstr)
