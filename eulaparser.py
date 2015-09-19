#!/usr/bin/python
import os, sys, re

class eulaParagraph:
    def __init__(self, hdr, para):
        self.header = hdr
        self.paragraph = para

    header = ''
    paragraph = ''

class paraProcesser(object):
    def __init__(self, para):
        self.paragraph = para

    def pprocess(para):
        fin2 = open('worthless.txt', 'r')
        lines = para
        passage = ''
        for x in lines:
    	       passage = passage + x
        passage = passage.replace('\n', '')
        origSentences = passage.split('.')
        for x in origSentences:
            x = x + '.'
        passage = passage.replace(',', '')
        sentences = passage.split('.')
        for x in sentences:
            x = x.replace('.','')
        passage = passage.replace('.', '')
        passage = passage.lower()
        words = passage.split()
        wordcount = {}
        for x in words:
            if x in wordcount:
                wordcount[x] += 1
            else:
                wordcount[x] = 1

        lines2 = fin2.readlines()
        for x in range(len(lines2)):
    	       lines2[x] = lines2[x].replace('\n','')
        for x in lines2:
    	       if x in wordcount:
    	              wordcount[x] = 0
        sentenceparts = []
        for x in sentences:
            sentenceparts.append((x.lower()).split())
        sentencescore = []
        for x in sentenceparts:
            total = 0
            for y in x:
                if y in wordcount:
                    total += wordcount[y]
            sentencescore.append(total)

        highscore  = 0
        for x in sentencescore:
            if x > highscore:
                highscore = x
        answer = ''
        for x in range(len(sentences)):
            if sentencescore[x] > highscore/2:
                answer = answer + origSentences[x]
        fin2.close()
        return answer

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

    paragrapher = paraProcesser()
    for p in sections:
        print "-"*25 + p.header + "-"*25
        print pararapher.pprocess(p.paragraph)

"""
for p in sections:
    print "-"*25 + p.header + "-"*25
    print p.paragraph
"""
