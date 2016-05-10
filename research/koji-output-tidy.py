#!/usr/bin/env python2

import os
import sys
import re

LINE_PREF = re.compile(r"(body|reply|send): ['\"](.+)['\"]")
HEADER_PREF = re.compile(r"header: (.+)")
R_N = re.compile(r"\\r\\n")
N = re.compile(r"\\n")
NEW = "\n"

if len(sys.argv) < 3:
	print "Usage: %s <input-file> <output-file-prefix>" % sys.argv[0]
	sys.exit(1)

INFILE=sys.argv[1]
OUTFILE_PREFIX=sys.argv[2]

def outname(count):
	return "%s-%s.txt" % (OUTFILE_PREFIX, count)

def open_output(count):
	path = os.path.join( os.getcwd(), outname(count) )
	d = os.path.dirname(path)

	if os.path.isdir(d) is False:
		os.makedirs(d)

	return open(path, 'w')

count = 1
linecount = 0
with open(INFILE) as f:
	print "Opening %s" % outname(count)
	outfile = open_output(count)
	for line in f:
		if linecount > 0 and line.lstrip().startswith("send: 'POST "):
			print "Closing %s (%s lines)" % (outname(count), linecount)
			count += 1
			print "Opening %s" % outname(count)
			outfile.close()
			outfile = open_output(count)
			linecount = 0
			continue
		out = line.rstrip()
		out = LINE_PREF.sub("\\2", out)
		out = HEADER_PREF.sub("\\1", out)
		out = R_N.sub(NEW, out)
		out = N.sub(NEW, out)
		outfile.write("%s\n" % out)
		linecount += 1
	print "Closing %s (%s lines)" % (outname(count), linecount)
	outfile.close()

