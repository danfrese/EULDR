#!/usr/bin/python
import os, sys, re

class eulaParagraph:
    def __init__(self, hdr, para):
        self.header = hdr
        self.paragraph = para

    header = ''
    paragraph = ''

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "Please enter an EULA file."
        sys.exit(-1)
    hfile = open(sys.argv[1], "r")

    sections = []
    headings = []

    pattern = re.compile(r'((^\s*)(([0-9]*)|([a-z])?)\.)')
    data = ''
    line = hfile.readline()
    while line:
        data += line
        if pattern.match(line):
            headings.append(line.strip())
        line = hfile.readline()

    hfile.close()

    offset = 0
    index = 0
    for heading in headings:
        begin = data.find(heading, offset) + len(heading)
        offset = begin

        if index+1 < len(headings):
            end = data.find(headings[index+1])
        else:
            end = len(data)
        para = data[begin:end]

        sections.append(eulaParagraph(heading, para))
        index += 1


for p in sections:
    print "-"*25 + p.header + "-"*25
    print p.paragraph
