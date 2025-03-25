#!/usr/bin/env python3
import sys
import os
from math import radians, sin, cos, sqrt, atan2

# point: (a, b), max distance: X
a = float(os.getenv('REF_LATITUDE', '0'))
b = float(os.getenv('REF_LONGITUDE', '0'))
X = float(os.getenv('REF_RADIUS', '1'))

print(f"Reference point: ({a}, {b}), max distance: {X} km", file=sys.stderr)

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    return R * (2 * atan2(sqrt(a), sqrt(1 - a)))

for line in sys.stdin:
    fields = line.strip().split(',')
    if len(fields) != 7:
        print(f"Invalid input: {fields}", file=sys.stderr)
        continue

    sensor_id, lat, lon, sensor_type, unit, timestamp, value = fields
    lat, lon, value = float(lat), float(lon), float(value)

    distance = haversine(a, b, lat, lon)
    print(f"DEBUG: Distance to point ({lat}, {lon}) is {distance:.2f} km", file=sys.stderr)

    if distance <= X:
        print(f"{sensor_type}\t{value}")
