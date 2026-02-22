from datetime import datetime, date
import re

DISPLAY_FMT = "%d.%m.%Y"
ISO_FMT = "%Y-%m-%d"

period_re = re.compile(r'^\s*(\d{2}\.\d{2}\.\d{4})\s*-\s*(\d{2}\.\d{2}\.\d{4})\s*$')

def display_date(d: date) -> str:
    return d.strftime(DISPLAY_FMT)

def to_iso(d: date) -> str:
    return d.strftime(ISO_FMT)

def parse_display_date(s: str) -> date:
    return datetime.strptime(s.strip(), DISPLAY_FMT).date()

def parse_period(text: str):
    m = period_re.match(text)
    if not m:
        return None, None
    try:
        start = parse_display_date(m.group(1))
        end = parse_display_date(m.group(2))
        if end < start:
            return None, None
        return start, end
    except Exception:
        return None, None