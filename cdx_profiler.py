#!/usr/bin/env python

# Author: Sawood Alam <ibnesayeed@gmail.com>
#
# This script processes CDX file(s) and extracts statistics to updtae a Profile object.

import os

os.environ["TLDEXTRACT_CACHE"] = "/tmp/.tld_set"

from suburi_generator import generate_suburis
from collections import namedtuple, defaultdict
from urlparse import urlparse
from surt import surt
import sys
import tldextract
import time

class CDXProfiler(object):
    """Profiling an archive using CDX files."""

    def __init__(self, max_host_segments=3, max_path_segments=0, global_stats=False):
        """Initialize with a basic object to store stats."""
        print("Initializing CDX profiler...")
        try:
            self.max_host_segments = int(max_host_segments)
        except ValueError:
            self.max_host_segments = None
        try:
            self.max_path_segments = int(max_path_segments)
        except ValueError:
            self.max_path_segments = None
        self.global_stats = global_stats
        self.total_lines = 0
        self.skipped_lines = 0
        self.stats = {"suburi": {}, "time": {}, "mediatype": {}, "language": {}}

    def process_cdxes(self, cdxs):
        """Accepts a list of CDX file names/paths and calls CDX processor on them."""
        print("CDX processing started...")
        for cdx in cdxs:
            self._process_cdx(cdx)

    def calculate_stats(self):
        """Calculates statistics from the raw profile data structure and prepares the profile object for serialization."""
        print("Calculating statistics...")
        self._calculate_section_stats(self.stats["suburi"])
        self._calculate_section_stats(self.stats["time"])
        self._calculate_section_stats(self.stats["mediatype"])
        if self.global_stats:
            self._calculate_global_stats()

    def _process_cdx(self, cdx):
        """Accepts a CDX file and processes it to extract neccessary information and builds a raw data structure."""
        print("Processing CDX: " + cdx)
        with open(cdx) as f:
            for line in f:
                entry = self._parse_line(line)
                self.total_lines += 1
                if entry and entry.scheme.startswith("http"):
                    self._update_ds(entry)
                else:
                    self.skipped_lines += 1

    def _parse_line(self, line=""):
        """Parses single line of a CDX file and returns selected and derived attributes in a namedtuple."""
        segs = line.strip().split(" ")
        if len(segs) == 10:
            url = urlparse(segs[2])
            dom = tldextract.extract(segs[2])
            Segments = namedtuple("Segments", "scheme, host, domain, tld, surt, uri, time, mime")
            return Segments(url.scheme, url.netloc, surt(dom.registered_domain), surt(dom.suffix), surt(segs[0]), segs[0], segs[1], segs[3])

    def _update_ds(self, entry):
        """Update data structure after processing a line from the CDX"""
        suburis = generate_suburis(entry.surt, max_host_segments=self.max_host_segments, max_path_segments=self.max_path_segments)
        for s in suburis:
            self._update_record("suburi", s, entry.surt)
        self._update_record("time", entry.time[0:6], entry.surt)
        self._update_record("mediatype", entry.mime, entry.surt)

    def _update_record(self, key_type, key, surt):
        """Insert or update raw records to keep track of URI-R and URI-M counts under each key."""
        entry_point = self.stats[key_type]
        try:
            entry_point[key]["surt"][surt] += 1
        except KeyError, e:
            if e.message == key:
                entry_point[key] = {"surt": {surt: 1}}
            if e.message == surt:
                entry_point[key]["surt"][surt] = 1

    def _calculate_section_stats(self, section):
        """Consume raw datastrcuture to calculate summarized statistics of each section."""
        for e in section.itervalues():
            s = e["surt"].values()
            count = len(s)
            total = sum(s)
            minm = min(s)
            maxm = max(s)
            e["urir"] = count
            e["urim"] = {"total": total, "min": minm, "max": maxm}
            del e["surt"]

    def _calculate_global_stats(self):
        """Accumulate TLD stats to calculate global summarized statistics."""
        count, total, minm, maxm = 0, 0, 1, 1
        for k, v in self.stats["suburi"].iteritems():
            if k.count(",") == 0:
                count += v["urir"]
                total += v["urim"]["total"]
                minm = min(minm, v["urim"]["min"])
                maxm = max(maxm, v["urim"]["max"])
        self.stats["urir"] = count
        self.stats["urim"] = {"total": total, "min": minm, "max": maxm}
