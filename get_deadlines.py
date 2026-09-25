import sys
import os

sys.path.append(os.path.dirname(__file__))
from get_calendar import get_calendar


def get_deadlines():
    """
    Shortcut for 'what's urgent' — just calls get_calendar with a
    short window (next 3 days) so it only shows near-term deadlines.
    """
    return get_calendar(days=3)