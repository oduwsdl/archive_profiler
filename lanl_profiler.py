#!/usr/bin/env python

# Author: Sawood Alam <ibnesayeed@gmail.com>
#
# This scripts transforms URIs to Digest Suffix formats.

import os
import sys
import time
import re
import tldextract
from urlparse import urlparse

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n[USAGE] ./lanl_profiler.py file-with-list-of-urls\n")
        sys.exit(0)
    url_file = sys.argv[1]
    url_file_name = os.path.splitext(url_file)[0]
    print("\n{0} => Converting {1}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"), url_file))
    gen_start = time.time()
    segsf = open(url_file_name + ".segs", "w")
    onlydomf = open(url_file_name + ".onlydom", "w")
    tillsubdomf = open(url_file_name + ".tillsubdom", "w")
    tillpathf = open(url_file_name + ".tillpath", "w")
    tillqueryf = open(url_file_name + ".tillquery", "w")
    tillinitf = open(url_file_name + ".tillinit", "w")
    pathqueryf = open(url_file_name + ".pathquery", "w")
    pathquerysuppinitf = open(url_file_name + ".pathquerysuppinit", "w")
    fail_count = 0
    with open(url_file) as f:
        for line in f:
            try:
                ext = tldextract.extract(line)
                urlseg = urlparse("http://" + line)
                subdom_len = path_len = query_len = 0
                path_init = suppressive_path_init = "-"
                reg_dom = ext.registered_domain.lower()
                reg_dom = re.sub('[^a-z0-9_\-\.]', '', reg_dom)
                first_path_char = urlseg.path.strip("\n\r/")[:1]
                if ext.subdomain:
                    subdom_len = ext.subdomain.count(".") + 1
                if urlseg.path:
                    path_len = urlseg.path.strip("\n\r/").count("/") + 1
                if urlseg.query:
                    query_len = urlseg.query.strip("?&").count("&") + 1
                if first_path_char:
                    path_init = re.sub('[^a-zA-Z0-9]', '-', first_path_char)
                    suppressive_path_init = re.sub('[^a-z]', '-', first_path_char.lower())
                segsf.write("{0} {1} {2} {3} {4} {5} {6}\n".format(reg_dom, subdom_len, path_len, query_len, path_len + query_len, path_init, suppressive_path_init))
                onlydomf.write("{0}\n".format(reg_dom))
                tillsubdomf.write("{0}/{1}\n".format(reg_dom, subdom_len))
                tillpathf.write("{0}/{1}/{2}\n".format(reg_dom, subdom_len, path_len))
                tillqueryf.write("{0}/{1}/{2}/{3}\n".format(reg_dom, subdom_len, path_len, query_len))
                tillinitf.write("{0}/{1}/{2}/{3}/{4}\n".format(reg_dom, subdom_len, path_len, query_len, path_init))
                pathqueryf.write("{0}/{1}/{2}\n".format(reg_dom, subdom_len, path_len + query_len))
                pathquerysuppinitf.write("{0}/{1}/{2}/{3}\n".format(reg_dom, subdom_len, path_len + query_len, suppressive_path_init))
            except Exception as e:
                print("Something went wrong while processing:\n => " + line)
                fail_count += 1
    segsf.close()
    onlydomf.close()
    tillsubdomf.close()
    tillpathf.close()
    tillqueryf.close()
    tillinitf.close()
    pathqueryf.close()
    pathquerysuppinitf.close()
    gen_end = time.time()
    print("Faild {0} times".format(fail_count))
    print("It took {0} minutes.".format(round((gen_end - gen_start)/60, 2)))
    print("All Done!")
