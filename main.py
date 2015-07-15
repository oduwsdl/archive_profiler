#!/usr/bin/env python

# Author: Sawood Alam <ibnesayeed@gmail.com>
#
# This scripts generates one or more profiles from the same collection with different policies based on the configurations.

import os
import sys
import gzip
import json
import time
import re
import ConfigParser

from profile import Profile
from key_generator import KeyGenerator

def build_profile(policy):
    print("{0} => Profiling with policy {1}".format(time.strftime("%Y-%m-%d %H:%M:%S"), policy))
    p = Profile(name=config.get("archive", "name"),
                description=config.get("archive", "description"),
                homepage=config.get("archive", "homepage"),
                accesspoint=config.get("archive", "accesspoint"),
                memento_compliance=config.get("archive", "memento_compliance"),
                timegate=config.get("archive", "timegate"),
                timemap=config.get("archive", "timemap"),
                established=config.get("archive", "established"),
                profile_updated=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                source="cdx",
                type="urikey#{0}".format(policy))
    opkfn = "intermediate-{0}.keys".format(policy)
    opkfpath = os.path.join(tempdir, opkfn)
    print("{0} => Storing intermediate keys in {1}".format(time.strftime("%Y-%m-%d %H:%M:%S"), opkfpath))
    opkf = open(opkfpath, "w")
    kg = KeyGenerator(policy)
    kg.generate_keys_from_files(sys.argv[1:], opkf)
    opkf.close()
    oppfn = "profile-{0}.cdxj".format(policy)
    oppfpath = os.path.join(profiledir, oppfn)
    print("{0} => Generating profile in {1}".format(time.strftime("%Y-%m-%d %H:%M:%S"), oppfpath))
    oppf = open(oppfpath, "w")
    preamble = "@context https://oduwsdl.github.io/contexts/archiveprofile.jsonld\n@id {0}\n".format(p.about["homepage"])
    pabout = json.dumps(p.about, sort_keys=True)
    oppf.write(preamble + "@about " + pabout + "\n")
    oppf.close()
    os.system('LC_ALL=C sort ' + opkfpath + ' | uniq -c | awk \'{ print $2 " {\\"frequency\\": "$1", \\"spread\\": 1}" }\' >> ' + oppfpath)
    print("{0} => Storing compressed profile in {1}".format(time.strftime("%Y-%m-%d %H:%M:%S"), oppfpath + ".gz"))
    os.system('gzip -c ' + oppfpath + ' > ' + oppfpath + '.gz')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nPlease do not forget to customize the config.ini file.\nUsage:\n  ./main.py /path/to/cdx/*.cdx\n")
        sys.exit(0)
    print("\n{0} => Profiling: {1}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"), sys.argv))
    scriptdir = os.path.dirname(os.path.abspath(__file__))
    config = ConfigParser.ConfigParser()
    config.read(os.path.join(scriptdir, "config.ini"))
    if config.get("archive", "name") == "Test Archive":
        print("WARNING: You should update the config.ini file, unless it is a test run.\n")
    profiledir = os.path.join(scriptdir, "profiles")
    if not os.path.exists(profiledir):
        os.makedirs(profiledir)
    tempdir = os.path.join(scriptdir, "tmp")
    if not os.path.exists(tempdir):
        os.makedirs(tempdir)
    policies = config.get("profile", "policies").split()
    for policy in policies:
        build_profile(policy)
    print("{0} => All Done!".format(time.strftime("%Y-%m-%d %H:%M:%S")))
