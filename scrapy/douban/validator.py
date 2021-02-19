import re

import arrow


def match_year(s):
    matches = re.findall("[\\d]{4}", s)
    if matches:
        return matches[0]
    else:
        return "0"


def match_date(s):
    matches = re.findall("[\\d-]{8,10}", s)
    if matches:
        return matches[0]
    else:
        return False


def str_to_date(s):
    try:
        return str(arrow.get(s, "YYYY-M-D").format("YYYY-MM-DD"))
    except Exception:
        return False


def is_match_chinese(s):
    matches = re.findall("[\u4e00-\u9fa5]+", s)
    if matches:
        return True
    else:
        return False


def process_slash_str(s):
    alias = []
    items = s.split("/")
    for item in items:
        if is_match_chinese(item):
            alias.append(item)
    return "/".join(alias[0:30])


def process_url(s):
    if len(s) < 255:
        return s
    return ""
