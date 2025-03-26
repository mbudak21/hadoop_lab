#!/usr/bin/env python3
import sys

values = []

for line in sys.stdin:
    sensor_type, value = line.strip().split('\t')
    values.append(float(value))

if values:
    print(f"Min\t{min(values)}")
    print(f"Max\t{max(values)}")
    print(f"Average\t{sum(values)/len(values):.2f}")
