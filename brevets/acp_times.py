"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

# Each row: (start km, end km, min speed, max speed)
SPEED_TABLE = [
    (0, 200, 15, 34),
    (200, 400, 15, 32),
    (400, 600, 15, 30),
    (600, 1000, 11.428, 28),
]

# Fixed overall time limits (hours) for the finish control
FINAL_CLOSE = {200: 13.5, 300: 20, 400: 27, 600: 40, 1000: 75}


def _open_hours(control_dist_km):
    hours = 0
    for row_start, row_end, min_speed, max_speed in SPEED_TABLE:
        km_in_row = min(control_dist_km, row_end) - row_start
        if km_in_row <= 0:
            break
        hours += km_in_row / max_speed
    return hours


def _close_hours(control_dist_km, brevet_dist_km):
    if control_dist_km >= brevet_dist_km:
        return FINAL_CLOSE[brevet_dist_km]
    if control_dist_km <= 60:
        return control_dist_km / 20 + 1
    hours = 0
    for row_start, row_end, min_speed, max_speed in SPEED_TABLE:
        km_in_row = min(control_dist_km, row_end) - row_start
        if km_in_row <= 0:
            break
        hours += km_in_row / min_speed
    return hours


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    control_dist_km = min(control_dist_km, brevet_dist_km)
    minutes = round(_open_hours(control_dist_km) * 60)
    return arrow.get(brevet_start_time).shift(minutes=minutes).isoformat()


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600, or 1000
           (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    minutes = round(_close_hours(control_dist_km, brevet_dist_km) * 60)
    return arrow.get(brevet_start_time).shift(minutes=minutes).isoformat()