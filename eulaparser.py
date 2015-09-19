
import os, sys, re
from sys import argv

class eulaParagraph(object):
    def __init__(self, hdr, para):
        self.header = hdr
        self.paragraph = para

    header = ''
    paragraph = ''

    # breaks down the given paragraph and displays the general idea of it
    def pprocess(self, para):
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
    # Asks for filename.txt
    if len(sys.argv) == 1:
        print "Please enter an EULA file."
        #sys.exit(-1)
    hfile = open(sys.argv[1], "r")

    # heading and paragraph vars used by the paragrapher object
    new_heading = ''
    para = ''

    headings = []                   # array of headings
    sections = []                   # array of sections

    #Regex operators to find heading pattern in given file.txt
    # TODO(@Zack) Need to adjust for EULAs that don't fall under this style format
    pattern = re.compile(r'((^\s*)(([0-9]*)|([a-z])?)\.)')
    data = ''
    line = hfile.readline()
    # Append qualifying line to header list
    while line:
        data += line
        if pattern.match(line):
            headings.append(line.strip())
        line = hfile.readline()

    hfile.close()

    offset = 0
    index = 0
    # Associate text paragraphs to heading entries
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
        new_heading = heading
    """
    paragrapher = eulaParagraph(new_heading, para)
    for p in sections:
        print "-"*25 + p.header + "-"*25
        print pararapher.pprocess(p.paragraph)
    """

#paragrapher = eulaParagraph(new_heading, sections)
paragrapher = eulaParagraph(new_heading, para)
for p in sections:
    print "-"*25 + p.header + "-"*25 # this works fine
    print paragrapher.pprocess(p.paragraph) # this prints the subheadings in section 17

"""
for p in sections:
    print "-"*25 + p.header + "-"*25
    print p.paragraph
"""
