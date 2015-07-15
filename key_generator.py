#!/usr/bin/env python

# Author: Sawood Alam <ibnesayeed@gmail.com>
#
# This class selects appropriate methdos for generating keys based on the policy.

import re
import time
import tldextract
from urlparse import urlparse
from surt import surt

class KeyGenerator(object):
    """Bind Profiler method based on the policy."""

    def __init__(self, policy="H1P0"):
        """Initialize a basic archive profile object."""
        print("{0} => Initializing the profiler with policy {1}".format(time.strftime("%Y-%m-%d %H:%M:%S"), policy))
        self.policy_map = {
            "HmPn": self._hmpn,
            "DDom": self._ddom,
            "DSub": self._dsub,
            "DPth": self._dpth,
            "DQry": self._dqry,
            "DIni": self._dini
        }
        self.policy = policy
        self.options = {}
        pattern = re.compile("^H(?P<host>\d+|x)P(?P<path>\d+|x)$")
        match = pattern.match(policy)
        if match:
            try:
                self.options["max_host_segments"] = int(match.group("host"))
            except ValueError:
                self.options["max_host_segments"] = None
            try:
                self.options["max_path_segments"] = int(match.group("path"))
            except ValueError:
                self.options["max_path_segments"] = None
            policy = "HmPn"
        try:
            self.generate_key = self.policy_map[policy]
        except KeyError:
            raise ValueError("Unrecognized profiling policy: {0}".format(self.policy))

    def _hmpn(self, url):
        return self._suburi(surt(url), max_host_segments=self.options["max_host_segments"], max_path_segments=self.options["max_path_segments"])

    def _ddom(self, url):
        ext = tldextract.extract(url)
        urlseg = urlparse("http://" + url)
        reg_dom = surt(ext.registered_domain)
        if reg_dom[0].isalpha():
            return reg_dom

    def _dsub(self, url):
        ext = tldextract.extract(url)
        urlseg = urlparse("http://" + url)
        reg_dom = surt(ext.registered_domain)
        if reg_dom[0].isalpha():
            subdom_len = 0
            if ext.subdomain:
                subdom_len = ext.subdomain.count(".") + 1
            return "{0}{1}".format(reg_dom, subdom_len)

    def _dpth(self, url):
        ext = tldextract.extract(url)
        urlseg = urlparse("http://" + url)
        reg_dom = surt(ext.registered_domain)
        if reg_dom[0].isalpha():
            subdom_len = path_len = 0
            if ext.subdomain:
                subdom_len = ext.subdomain.count(".") + 1
            if urlseg.path:
                path_len = urlseg.path.strip("\n\r/").count("/") + 1
            return "{0}{1}/{2}".format(reg_dom, subdom_len, path_len)

    def _dqry(self, url):
        ext = tldextract.extract(url)
        urlseg = urlparse("http://" + url)
        reg_dom = surt(ext.registered_domain)
        if reg_dom[0].isalpha():
            subdom_len = path_len = query_len = 0
            if ext.subdomain:
                subdom_len = ext.subdomain.count(".") + 1
            if urlseg.path:
                path_len = urlseg.path.strip("\n\r/").count("/") + 1
            if urlseg.query:
                query_len = urlseg.query.strip("?&").count("&") + 1
            return "{0}{1}/{2}/{3}".format(reg_dom, subdom_len, path_len, query_len)

    def _dini(self, url):
        ext = tldextract.extract(url)
        urlseg = urlparse("http://" + url)
        reg_dom = surt(ext.registered_domain)
        if reg_dom[0].isalpha():
            subdom_len = path_len = query_len = 0
            path_init = urlseg.path.strip("\n\r/")[:1]
            if ext.subdomain:
                subdom_len = ext.subdomain.count(".") + 1
            if urlseg.path:
                path_len = urlseg.path.strip("\n\r/").count("/") + 1
            if urlseg.query:
                query_len = urlseg.query.strip("?&").count("&") + 1
            if not path_init.isalnum():
                path_init = "-"
            return "{0}{1}/{2}/{3}/{4}".format(reg_dom, subdom_len, path_len, query_len, path_init)

    def _suburi(self, surt, max_host_segments=None, max_path_segments=None):
        if surt[:2].isalpha():
            host, path = surt.split("?")[0].split(")", 1)
            host_segments = host.strip(",").split(",")
            if not isinstance(max_host_segments, int):
                max_host_segments = len(host_segments)
            if len(host_segments) > max_host_segments:
                return ",".join(host_segments[0:max_host_segments]) + ")/"
            path_segments = path.strip("/").split("/")
            if not isinstance(max_path_segments, int):
                max_path_segments = len(path_segments)
            return host + ")/" + "/".join(path_segments[0:max_path_segments])

    def generate_keys_from_files(self, inputs, output):
        for inp in inputs:
            print("{0} => Generating keys from {1}".format(time.strftime("%Y-%m-%d %H:%M:%S"), inp))
            with open(inp) as f:
                for line in f:
                    k = self.generate_key(line.split(" ")[0])
                    if k:
                        output.write(k + "\n")

if __name__ == "__main__":
    print("Pass a policy parameter to create an object of KeyGenerator class then call generate_key or generate_keys_from_files methods on it.")
