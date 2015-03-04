#!/usr/bin/env python

# Author: Sawood Alam <ibnesayeed@gmail.com>
#
# This scripts instantiate two Profile objects, populates one or both from a JSON profile(s), merges them, and serializes merged profile in JSON.

import os
import sys
import pprint
import json
import time
import requests
import ConfigParser

from profile import Profile

def print_help():
    """Print help text."""
    print("\nTo merge JSON profile(s):")
    print("  Start with the empty base profile :    profile_merger.py output.json first.json")
    print("  Merge new to the base profile     :    profile_merger.py output.json new.json base.json")

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
    if len(sys.argv) not in [3, 4]:
        print_help()
        sys.exit(0)
    p_new = Profile()
    p_new.load(open(sys.argv[2]))
    p_base = Profile()
    p_base.about = p_new.about
    p_base.stats["suburi"] = {}
    if len(sys.argv) == 4:
        p_base.load(open(sys.argv[3]))
    section = p_base.stats["suburi"]
    for k, v in p_new.stats["suburi"].iteritems():
        if k in section:
            section[k]["urir_sum"] += v["urir"]
            section[k]["sources"] += 1
        else:
            section[k] = {"urir_sum": v["urir"], "sources": 1}
    jsonstr = p_base.to_json()
    write_json(jsonstr, filepath=sys.argv[1])
#    print(jsonstr)
