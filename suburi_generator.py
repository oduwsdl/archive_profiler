#!/usr/bin/env python

def generate_suburis(surt, max_host_segments=None, max_path_segments=None):
    host, path = surt.split("?")[0].split(")", 1)
    suburis = []
    host_segments = host.strip(",").split(",")
    include_path = True
    for i in range(0, len(host_segments)):
        if i == max_host_segments:
            include_path = False
            break
        suburis.append(",".join(host_segments[0:i+1]) + ")/")
    path_segments = path.strip("/").split("/")
    if include_path:
        for i in range(0, len(path_segments)):
            if i == max_path_segments:
                break
            suburis.append(host + ")/" + "/".join(path_segments[0:i+1]))
    return sorted(set(suburis))

if __name__ == "__main__":
    import pytest
    pytest.main()
