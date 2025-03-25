#!/usr/bin/env python3
import sys
import string

# read input from standard input line by line
for line in sys.stdin:
	# remove punctuation
	for pnct in list(string.punctuation):
		line = line.replace(pnct,' ')
	# split line into words
	words = line.strip().split()
	# for each word produce the pair with count equal to 1 separated by a tab 
	for word in words:
		print(f"{word}\t1")