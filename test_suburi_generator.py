#!/usr/bin/env python

from suburi_generator import generate_suburis

sample = [{
    "surt": "com,example,domain,sub)/p1/p2/file.ext?a=b&c=d",
    "suburis": [
        "com)/",
        "com,example)/",
        "com,example,domain)/",
        "com,example,domain,sub)/",
        "com,example,domain,sub)/p1",
        "com,example,domain,sub)/p1/p2",
        "com,example,domain,sub)/p1/p2/file.ext"
    ]
}, {
    "surt": "com,example)/p1/file_(1).ext?a=b&c=d",
    "suburis": [
        "com)/",
        "com,example)/",
        "com,example)/p1",
        "com,example)/p1/file_(1).ext"
    ]
}]

def test_zero_host_zero_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=0, max_path_segments=0) == []

def test_zero_host_one_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=0, max_path_segments=1) == []

def test_zero_host_middle_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=0, max_path_segments=2) == []

def test_zero_host_equal_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=0, max_path_segments=3) == []

def test_zero_host_more_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=0, max_path_segments=4) == []
    assert generate_suburis(sample[0]["surt"], max_host_segments=0, max_path_segments=6) == []

def test_zero_host_all_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=0) == []

def test_one_host_zero_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=1, max_path_segments=0) == sample[0]["suburis"][0:1]

def test_one_host_one_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=1, max_path_segments=1) == sample[0]["suburis"][0:1]

def test_one_host_middle_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=1, max_path_segments=2) == sample[0]["suburis"][0:1]

def test_one_host_equal_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=1, max_path_segments=3) == sample[0]["suburis"][0:1]

def test_one_host_more_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=1, max_path_segments=4) == sample[0]["suburis"][0:1]
    assert generate_suburis(sample[0]["surt"], max_host_segments=1, max_path_segments=6) == sample[0]["suburis"][0:1]

def test_one_host_all_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=1) == sample[0]["suburis"][0:1]

def test_middle_host_zero_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=2, max_path_segments=0) == sample[0]["suburis"][0:2]

def test_middle_host_one_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=2, max_path_segments=1) == sample[0]["suburis"][0:2]

def test_middle_host_middle_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=2, max_path_segments=2) == sample[0]["suburis"][0:2]

def test_middle_host_equal_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=2, max_path_segments=3) == sample[0]["suburis"][0:2]

def test_middle_host_more_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=2, max_path_segments=4) == sample[0]["suburis"][0:2]
    assert generate_suburis(sample[0]["surt"], max_host_segments=2, max_path_segments=6) == sample[0]["suburis"][0:2]

def test_middle_host_all_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=2) == sample[0]["suburis"][0:2]

def test_equal_host_zero_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=4, max_path_segments=0) == sample[0]["suburis"][0:4]

def test_equal_host_one_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=4, max_path_segments=1) == sample[0]["suburis"][0:5]

def test_equal_host_middle_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=4, max_path_segments=2) == sample[0]["suburis"][0:6]

def test_equal_host_equal_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=4, max_path_segments=3) == sample[0]["suburis"]

def test_equal_host_more_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=4, max_path_segments=4) == sample[0]["suburis"]
    assert generate_suburis(sample[0]["surt"], max_host_segments=4, max_path_segments=6) == sample[0]["suburis"]

def test_equal_host_all_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=4) == sample[0]["suburis"]

def test_more_host_zero_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=5, max_path_segments=0) == sample[0]["suburis"][0:4]
    assert generate_suburis(sample[0]["surt"], max_host_segments=7, max_path_segments=0) == sample[0]["suburis"][0:4]

def test_more_host_one_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=5, max_path_segments=1) == sample[0]["suburis"][0:5]
    assert generate_suburis(sample[0]["surt"], max_host_segments=7, max_path_segments=1) == sample[0]["suburis"][0:5]

def test_more_host_middle_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=5, max_path_segments=2) == sample[0]["suburis"][0:6]
    assert generate_suburis(sample[0]["surt"], max_host_segments=7, max_path_segments=2) == sample[0]["suburis"][0:6]

def test_more_host_equal_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=5, max_path_segments=3) == sample[0]["suburis"]
    assert generate_suburis(sample[0]["surt"], max_host_segments=7, max_path_segments=3) == sample[0]["suburis"]

def test_more_host_more_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=5, max_path_segments=4) == sample[0]["suburis"]
    assert generate_suburis(sample[0]["surt"], max_host_segments=7, max_path_segments=4) == sample[0]["suburis"]
    assert generate_suburis(sample[0]["surt"], max_host_segments=5, max_path_segments=6) == sample[0]["suburis"]
    assert generate_suburis(sample[0]["surt"], max_host_segments=7, max_path_segments=6) == sample[0]["suburis"]

def test_more_host_all_path():
    assert generate_suburis(sample[0]["surt"], max_host_segments=5) == sample[0]["suburis"]
    assert generate_suburis(sample[0]["surt"], max_host_segments=7) == sample[0]["suburis"]

def test_all_host_zero_path():
    assert generate_suburis(sample[0]["surt"], max_path_segments=0) == sample[0]["suburis"][0:4]

def test_all_host_one_path():
    assert generate_suburis(sample[0]["surt"], max_path_segments=1) == sample[0]["suburis"][0:5]

def test_all_host_middle_path():
    assert generate_suburis(sample[0]["surt"], max_path_segments=2) == sample[0]["suburis"][0:6]

def test_all_host_equal_path():
    assert generate_suburis(sample[0]["surt"], max_path_segments=3) == sample[0]["suburis"]

def test_all_host_more_path():
    assert generate_suburis(sample[0]["surt"], max_path_segments=4) == sample[0]["suburis"]
    assert generate_suburis(sample[0]["surt"], max_path_segments=6) == sample[0]["suburis"]

def test_all_host_all_path():
    assert generate_suburis(sample[0]["surt"]) == sample[0]["suburis"]
    assert generate_suburis(sample[0]["surt"][:-7]) == sample[0]["suburis"]
    assert generate_suburis(sample[0]["surt"][:-8]) == sample[0]["suburis"]
    assert generate_suburis(sample[0]["surt"][:-16]) == sample[0]["suburis"][:-1]
    assert generate_suburis(sample[0]["surt"][:-17]) == sample[0]["suburis"][:-1]
    assert generate_suburis(sample[0]["surt"][:-19]) == sample[0]["suburis"][:-2]
    assert generate_suburis(sample[0]["surt"][:-20]) == sample[0]["suburis"][:-2]
    assert generate_suburis(sample[0]["surt"][:-22]) == sample[0]["suburis"][:-3]
    assert generate_suburis(sample[0]["surt"][:-28]+")/") == sample[0]["suburis"][:-4]
    assert generate_suburis(sample[0]["surt"][:-35]+")/") == sample[0]["suburis"][:-5]
    assert generate_suburis(sample[0]["surt"][:-43]+")/") == sample[0]["suburis"][:-6]

def test_explicit_none_param():
    assert generate_suburis(sample[0]["surt"], max_host_segments=None) == sample[0]["suburis"]
    assert generate_suburis(sample[0]["surt"], max_path_segments=None) == sample[0]["suburis"]
    assert generate_suburis(sample[0]["surt"], max_host_segments=None, max_path_segments=None) == sample[0]["suburis"]

def test_non_int_param():
    assert generate_suburis(sample[0]["surt"], max_host_segments="all") == sample[0]["suburis"]
    assert generate_suburis(sample[0]["surt"], max_path_segments="all") == sample[0]["suburis"]
    assert generate_suburis(sample[0]["surt"], max_host_segments="all", max_path_segments="all") == sample[0]["suburis"]

def test_paren_in_path():
    assert generate_suburis(sample[1]["surt"]) == sample[1]["suburis"]
