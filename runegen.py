#!/usr/bin/python

import re
import csv

names = {
         "<"  : "gal",
         ")"  : "per",
         "|"  : "bar",
         ">"  : "gar",
         "["  : "sel",
         "\\" : "bas",
         "#"  : "hax",
         ";"  : "sem",
         "$"  : "buc",
         "-"  : "hep",
         "]"  : "ser",
         "_"  : "cab",
         "{"  : "kel",
         "~"  : "sig",
         "%"  : "cen",
         "}"  : "ker",
         "'"  : "soq",
         ":"  : "col",
         "^"  : "ket",
         "*"  : "tar",
         ","  : "com",
         "+"  : "lus",
         "`"  : "tec",
         "\"" : "doq",
         "&"  : "pam",
         "="  : "tis",
         "."  : "dot",
         "@"  : "pat",
         "?"  : "wut",
         "/"  : "fas",
         "("  : "pel",
         "!"  : "zap"}

runef = open("runelist")
digraphs = []
phonemictexts = {}
symbols = {}
for line in runef:
	if len(line) < 3:
		continue
	digraph = line.strip()
	phonemictext = digraph
	for graph,text in names.iteritems():
		phonemictext = phonemictext.replace(graph,text)
	digraphs.append(digraph)
	phonemictexts[digraph] = phonemictext
	phonemictexts[phonemictexts[digraph]] = digraph
	symbols[digraph] = "%" + phonemictext[0] + phonemictext[2:4] + phonemictext[5]
	symbols[symbols[digraph]] = digraph

#for i,j,k in zip(digraphs,phonemictexts,symbols):
#	print i,k,j

hoonf = open("hoon.hoon")
genemode = False
genes = {}
for line in hoonf:
	if not genemode:
		if line[0:8] == "++  gene":
			genemode = True
		continue
	if line[0:2] == "++":
		break
	m = re.match(r'.*\[(%....) (.*)\].*',line)
	if not m:
		continue
	if not m.group(1) in symbols:
		continue
	genes[symbols[m.group(1)]] = m.group(0).strip()
	genes[genes[symbols[m.group(1)]]] = m.group(1)
hoonf.close()

hoonf = open("hoon.hoon")
apmode = False
aps = {}
for line in hoonf:
	if not apmode:
		if line[0:7] == "++  ap\n":
			apmode = True
		continue
	if line[0:2] == "++":
		break
	m = re.match(r'.*\[(%....) \*] {1,5}([^ ].*)',line)
	if not m:
		continue
	if not m.group(1) in symbols:
		continue
	aps[symbols[m.group(1)]] = m.group(0).strip()
	aps[aps[symbols[m.group(1)]]] = m.group(1)


# Save information to csv file
csvwriter = csv.writer(open('runes.csv','wb'),delimiter='\t',quoting=csv.QUOTE_MINIMAL,lineterminator='\n')
csvwriter.writerow(['digraph','symbol','name','gene','ap'])
for i in digraphs:
	csvwriter.writerow([i,symbols[i],phonemictexts[i], genes[i] if i in genes else '', aps[i] if i in aps else ''])

for i in digraphs:
	f = open("runes/" + phonemictexts[i] + ".txt",'w')
	f.write(i + "  " + symbols[i] + "   " + phonemictexts[i] + "\n")
	if i in genes:
		f.write("\n  gene:\n    " + genes[i] + "\n")
	if i in aps:
		f.write("\n  ap:\n    " + aps[i] + "\n")

