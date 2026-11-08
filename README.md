# ACP Brevet Control Times Calculator

A web replacement for the RUSA ACP brevet control time calculator
(https://rusa.org/octime_acp.html). Enter control distances and the
open and close times fill in automatically using Flask and Ajax.

## Author

Ruben Oramas, ruben.oramas05@gmail.com

## How the times are calculated

A brevet is a long-distance bike ride with checkpoints called controls.
Each control has an open time (the earliest a fast rider could arrive)
and a close time (the latest a slow rider can arrive). Both are measured
from the brevet's start time.

### Speed table

| Control location (km) | Minimum speed (km/h) | Maximum speed (km/h) |
|---|---|---|
| 0 to 200 | 15 | 34 |
| 200 to 400 | 15 | 32 |
| 400 to 600 | 15 | 30 |
| 600 to 1000 | 11.428 | 28 |

### Rules

1. **Open time** uses the maximum speeds. The speeds work like tax
   brackets: each stretch of distance is divided by the speed for its
   own row, and the pieces are added. For example, a control at 350 km
   opens at 200/34 + 150/32 = 10H34, not 350/32 = 10H56.
2. **Close time** uses the minimum speeds in the same way. For the first
   600 km this is simply distance / 15. For example, 350 km closes at
   350/15 = 23H20.
3. **Controls in the first 60 km** close at distance / 20 + 1 hour, which
   gives riders more time near the start. For example, 40 km closes at
   3H00. At exactly 60 km both formulas give 4H00. The start control
   (0 km) closes 1 hour after the start.
4. **The finish control** does not use the formula for its close time.
   It uses the fixed overall limit for the brevet distance:
   200 km = 13H30, 300 km = 20H00, 400 km = 27H00, 600 km = 40H00,
   1000 km = 75H00.
5. **Routes that run long:** a final control past the brevet distance
   (for example 205 km in a 200 km brevet) is calculated as if it were
   exactly the brevet distance. The rider gets no extra time.
6. **Rounding:** all times are rounded to the nearest minute.

Official brevet distances are 200, 300, 400, 600, and 1000 km.

## Running the app

With Docker, from the `brevets` folder:

    docker build -t brevets .
    docker run -d -p 5000:5000 brevets

Then open http://localhost:5000. (On a Mac where port 5000 is taken by
AirPlay, use `-p 8000:5000` and open http://localhost:8000.)

## Running the tests

From the `brevets` folder:

    pip install -r requirements.txt
    nosetests

The tests in `test_acp_times.py` each target one rule above and were
checked against the official RUSA calculator.

## For developers

- `acp_times.py`: the open and close time logic. `open_time` and
  `close_time` take a control distance, a brevet distance, and an
  ISO 8601 start time, and return an ISO 8601 time. The speed table is
  stored as data, so changing a speed means changing one row.
- `flask_brevets.py`: the Flask server. `/_calc_times` takes `km`,
  `brevet_dist_km`, and `start` as URL arguments and returns
  `{"result": {"open": ..., "close": ...}}` as JSON.
- `templates/calc.html`: the page. Its JavaScript sends a request with
  `$.getJSON` whenever a distance is entered and fills in the times.

Known limitation: changing the brevet distance or start time does not
update rows already filled in. Re-enter the distance to recalculate.