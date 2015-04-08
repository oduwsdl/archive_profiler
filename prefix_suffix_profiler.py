#!/usr/bin/env python

# Author: Sawood Alam <ibnesayeed@gmail.com>
#
# This scripts transforms URIs to Prefix and Suffix format.

import os
import sys
import time
import tldextract
from urlparse import urlparse

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n[USAGE] ./prefix_suffix_profiler.py list-of-urls.url\n")
        sys.exit(0)
    url_file = sys.argv[1]
    print("\n{0} => Converting {1}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"), url_file))
    gen_start = time.time()
    urif = open(url_file.replace(".url", ".urifix"), "w")
    urifp = open(url_file.replace(".url", ".urifixp"), "w")
    with open(url_file) as f:
        try:
            for line in f:
                ext = tldextract.extract(line)
                urlseg = urlparse(line)
                subdom_len = len([x for x in ext.subdomain.split(".") if x])
                path_len = len([x for x in urlseg.path.split("/") if x])
                query_len = len([x for x in urlseg.params.split("&") if x])
                first_path_char = urlseg.path.strip("\n\r/")[:1]
                urif.write("{0}/{1}/{2}\n".format(subdom_len, ext.registered_domain, path_len + query_len))
                urifp.write("{0}/{1}/{2}{3}\n".format(subdom_len, ext.registered_domain, first_path_char, path_len + query_len))
        except:
            print("Something went wrong while processing " + line)
    urif.close()
    urifp.close()
    gen_end = time.time()
    print("It took {0} minutes.".format(round((gen_end - gen_start)/60, 2)))
    print("All Done!")
