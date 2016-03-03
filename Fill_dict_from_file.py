#! /usr/bin/python
import sys

INPUT_FILE = str(sys.argv[1])
OUTPUT_FILE = str(sys.argv[2])
SERVICE_FILE = 'service.txt'
d = {}
f3 = open(SERVICE_FILE , "r" )
for line3 in f3:
    reader3 = line3.split('|')
    key = int(reader3[0])
    value = reader3[1]
    d[key] = value
f3.close()
print "Length : %d" % len (d)

fo = open(INPUT_FILE , "r" )
f2 = open(OUTPUT_FILE, "a")
for line in fo:
    reader = line.split('|')
    target = int(reader[1])
    if target in d.keys():
       f2.write(reader[0])
       f2.write("|")
       f2.write(reader[1])
       f2.write("|")
       f2.write(reader[2])
       f2.write("|")
       f2.write(reader[3])
       f2.write("|")
       f2.write(reader[4])
       f2.write("|")
       f2.write(d[target].rstrip())
       f2.write("|")
       f2.write(reader[6])
       f2.write("|")
       f2.write(reader[7])

    else:
       f2.write(line)
f2.close()
fo.close()
