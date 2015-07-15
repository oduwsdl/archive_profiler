#!/usr/bin/env python

# Author: Sawood Alam <ibnesayeed@gmail.com>
#
# This scripts transforms URIs to Prefix and Suffix format.

import os
import sys
import time
import re
import tldextract
from urlparse import urlparse

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n[USAGE] ./prefix_suffix_profiler.py list-of-urls.url\n")
        sys.exit(0)
    url_file = sys.argv[1]
    print("\n{0} => Converting {1}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"), url_file))
    gen_start = time.time()
    urif = open(url_file.replace(".urir", ".urifix"), "w")
    urifp = open(url_file.replace(".urir", ".urifixp"), "w")
    fil_count = 0
    with open(url_file) as f:
        for line in f:
            try:
                ext = tldextract.extract(line)
                urlseg = urlparse(line)
                reg_dom = ext.registered_domain.lower()
                reg_dom = re.sub('[^a-z0-9_\-\.]', '', reg_dom)
                subdom_len = len([x for x in ext.subdomain.split(".") if x])
                path_len = len([x for x in urlseg.path.split("/") if x])
                query_len = len([x for x in urlseg.params.split("&") if x])
                first_path_char = urlseg.path.strip("\n\r/")[:1]
                first_path_char = re.sub('[^a-zA-Z0-9_\-\.]', '', first_path_char)
                urif.write("{0}/{1}/{2}\n".format(subdom_len, reg_dom, path_len + query_len))
                urifp.write("{0}/{1}/{2}{3}\n".format(subdom_len, reg_dom, first_path_char, path_len + query_len))
            except Exception as e:
                print("Something went wrong while processing:\n => " + line)
                fil_count += 1
                urif.write("0/couldnotextract/0\n")
                urifp.write("0/couldnotextract/0\n")
    urif.close()
    urifp.close()
    gen_end = time.time()
    print("Faild {0} times".format(fil_count))
    print("It took {0} minutes.".format(round((gen_end - gen_start)/60, 2)))
    print("All Done!")
