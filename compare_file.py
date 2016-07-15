#! /usr/bin/python
import sys

#SERVICE_FILE- file tat need to be stored in dict
#INPUT_FILE - file to parse each time
#OUTPUT_FILE - file will write
INPUT_FILE = str(sys.argv[1])
OUTPUT_FILE = str(sys.argv[2])
SERVICE_FILE = str(sys.argv[3])
d = {}
f3 = open(SERVICE_FILE ,"r")
for line3 in f3:
    reader3 = line3.split(',')
    key = int(reader3[0])
    value = reader3[0]
    d[key] = value #This parse the file and keep it in dictionary(like map)
f3.close()
print "Length : %d" % len (d)

fo = open(INPUT_FILE , "r")
f2 = open(OUTPUT_FILE, "a")
for line in fo:
    reader = line.split(',')
    target = int(reader[0])
    if target in d.keys():
        f2.write(str(target))
        f2.write("\n")

f2.close()
fo.close()
