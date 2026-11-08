"""
Nose tests for acp_times.py
Expected values checked against the RUSA ACP calculator
(https://rusa.org/octime_acp.html) with a start of 2017-01-01 00:00.
"""
import acp_times

START = "2017-01-01T00:00:00+00:00"


def test_open_speed_changes_after_200():
    # 200/34 + 150/32 = 10H34. A shortcut of 350/32 would give 10H56.
    assert acp_times.open_time(350, 400, START) == "2017-01-01T10:34:00+00:00"


def test_close_finish_uses_fixed_limit():
    # Finish of a 400 km brevet is 27H00, not 400/15 = 26H40
    assert acp_times.close_time(400, 400, START) == "2017-01-02T03:00:00+00:00"


def test_close_intermediate_uses_formula():
    # Same 400 km, but in a 600 km brevet it's just a checkpoint: 26H40
    assert acp_times.close_time(400, 600, START) == "2017-01-02T02:40:00+00:00"


def test_close_first_60km_rule():
    # 40/20 + 1 = 3H00, not 40/15 = 2H40
    assert acp_times.close_time(40, 200, START) == "2017-01-01T03:00:00+00:00"


def test_start_control_closes_after_one_hour():
    assert acp_times.close_time(0, 200, START) == "2017-01-01T01:00:00+00:00"


def test_long_route_treated_as_brevet_distance():
    # 205 km finish of a 200 km brevet: open 5H53, close 13H30
    assert acp_times.open_time(205, 200, START) == "2017-01-01T05:53:00+00:00"
    assert acp_times.close_time(205, 200, START) == "2017-01-01T13:30:00+00:00"


def test_600_to_1000_range():
    # 890 km in a 1000 km brevet: open 29H09, close 65H23
    assert acp_times.open_time(890, 1000, START) == "2017-01-02T05:09:00+00:00"
    assert acp_times.close_time(890, 1000, START) == "2017-01-03T17:23:00+00:00"