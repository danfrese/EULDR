
import os, sys, re
from sys import argv

class eulaParagraph(object):
    def __init__(self, hdr, para):
        self.header = hdr
        self.paragraph = para

    header = ''
    paragraph = ''

    # GitHub was broken and didn't push the initial commit
    # breaks down the given paragraph and displays the general idea of it
    def pprocess(self, para):
        fin2 = open('worthless.txt', 'r')   # Opens the worthless dictionary to find useless wording
        lines = para                        # Set lines equal to the current paragraph being analyzed
        passage = ''                        # Initialize passage to hold the lines to be altered for the dictionary

        # Remove puncutation from the given paragraph
        for x in lines:                     # Add paragraph lines to the current passage string, useful with multiple paragraphs
    	       passage += x
        passage = passage.replace('\n', '') # Remove all newline chars
        origSentences = passage.split('.')  # Split and remove periods assigning values into an array
        for x in origSentences:             # Add the removed periods to all indexes
            x = x + '.'
        passage = passage.replace(',', '')  # Remove commas from passage
        sentences = passage.split('.')      # Split and remove periods assigning values into an array
        for x in sentences:                 # Remove all periods from sentences
            x = x.replace('.','')
        passage = passage.replace('.', '')  # Remove periods
        passage = passage.lower()           # Set all values to lowercase for easy parsing

        # Dictionary counter
        words = passage.split()             # Split the passage into a giant list of words
        wordcount = {}                      # Initializes a dictionary literal to hold word counts
        for x in words:                     # Populates the dictionary literal
            if x in wordcount:
                wordcount[x] += 1           # Add count to word
            else:
                wordcount[x] = 1            # Sets word count to 1 if not found in dictionary

        # Read in all lines and remove all newline characters
        lines2 = fin2.readlines()           # Assign all lines of a file to array lines2
        for x in range(len(lines2)):        # Generate a list of numbers to iterate over
    	       lines2[x] = lines2[x].replace('\n','')
        # Set all word counts back to 0 to prepare for the next reading
        for x in lines2:
    	       if x in wordcount:
    	              wordcount[x] = 0

        # Split into sentence parts to find the score of a sentence
        sentenceparts = []
        for x in sentences:                 # Append the sentence after lowercasing and splitting by spaces
            sentenceparts.append((x.lower()).split())
        sentencescore = []
        for x in sentenceparts:
            total = 0
            for y in x:
                if y in wordcount:
                    total += wordcount[y]
            sentencescore.append(total)

        # Look for the highest score from sentence's score to determine the most high value sentences
        # A sentence is more valuable if it uses words that appear more frequently in the paragraph
        highscore = 0
        for x in sentencescore:
            if x > highscore:
                highscore = x
        answer = ''
        # Iterate through sentences list to see if the score is higher than the high score#
        for x in range(len(sentences)):
            if sentencescore[x] > highscore/2:
                answer = answer + origSentences[x]
        fin2.close()
        return answer

if __name__ == '__main__':
    # Asks for filename.txt
    if len(sys.argv) == 1:
        print "Please enter an EULA file."
        sys.exit(-1)
    hfile = open(sys.argv[1], "r")

    # heading and paragraph vars used by the paragrapher object
    new_heading = ''
    para = ''

    headings = []                   # array of headings
    sections = []                   # array of sections

    #Regex operators to find heading pattern in given file.txt
    # TODO Need to adjust for EULAs that don't fall under this style format
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


paragrapher = eulaParagraph(new_heading, para)
for p in sections:
    print "-"*25 + p.header + "-"*25            # Prints the current header value
    print paragrapher.pprocess(p.paragraph)     # Prints the simplified paragraph under each heading
