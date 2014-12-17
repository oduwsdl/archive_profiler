#!/usr/bin/env python

# Author: Sawood Alam <ibnesayeed@gmail.com>
#
# This class creates structure of the profile, loads JSON profiles, and serializes the profile object to JSON.

import json

class Profile(object):
    """Basic archive profile to be evolved by the profiler."""

    def __init__(self, name="", description="", homepage="", accesspoint="", memento_compliance="", timegate="", timemap="", established="", profile_updated="", **kwargs):
        """Initialize a basic archive profile object."""
        print("Initializing the profile...")
        self.about = {
            "name": name,
            "description": description,
            "homepage": homepage,
            "accesspoint": accesspoint,
            "memento_compliance": memento_compliance,
            "timegate": timegate,
            "timemap": timemap,
            "established": established,
            "profile_updated": profile_updated
        }
        self.__dict__["about"].update(kwargs)
        self.stats = {}
        setattr(self, "@context", "https://oduwsdl.github.io/contexts/archiveprofile.jsonld")
        setattr(self, "@id", homepage)

    def load(self, json=None):
        """Load a JSON profile and populate the profile object"""
        print("TODO: Yet to implement!")

    def to_json(self):
        """Serializes processed profile object in JSON format."""
        print("Converting to JSNON...")
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4, separators=(',', ': '))

    def count_keys(self):
        """Generates statistics on profile keys."""
        print("Generating key statistics...")
        path = {}
        domain = {}
        for k in self.stats["suburi"].keys():
            path_depth = k.strip("/").count("/")
            if path_depth > 0:
                try:
                    path[path_depth] += 1
                except KeyError, e:
                    path[path_depth] = 1
            else:
                try:
                    domain[k.split(")")[0].count(",")+1] += 1
                except KeyError, e:
                    domain[k.split(")")[0].count(",")+1] = 1
        key_stats = {"time": len(self.stats["time"]),
                     "mediatype": len(self.stats["mediatype"]),
                     "language": len(self.stats["language"]),
                     "suburi": {"domain_depth": domain, "path_depth": path}}
        setattr(self, "_key_stats", key_stats)
        return key_stats
