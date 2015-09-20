# coding=UTF-8
from __future__ import division
import re, os, sys
from sys import argv

class SummaryTool(object):
    def __init__(self, hdr, content):
        self.header = hdr
        self.content = content

    header = ''
    content = ''

    # Split given chunk of text into sentences
    def split_content_to_sentences(self, content):
        content = content.replace("\n", ". ")
        return content.split(". ")

    """
        Purpose: Split given chunk of text into paragraphs
        This might cause code to fail on non Windows machines due to differences
        in how the originating OS encodes text files.
    """
    def split_content_to_paragraphs(self, content):
        return content.split("\n\n")

    # Caculate the intersection between 2 sentences
    # The intersection finds the number of times a word occurs between 2 sentences
    def sentences_intersection(self, sent1, sent2):

        # split the sentence into words/tokens
        sentenceToken1 = set(sent1.split(" "))
        sentenceToken2 = set(sent2.split(" "))

        # If there is not intersection, just return 0
        if (len(sentenceToken1) + len(sentenceToken2)) == 0:
            return 0

        # Normalize result by average counted words
        return len(sentenceToken1.intersection(sentenceToken2)) / ((len(sentenceToken1) + len(sentenceToken2)) / 2)

    # Remove all non-alphbetic ([a-z]|[A-Z]) characters from the sentence
    # The formatted sentence is used as key in our sentences dictionary
    def format_sentence(self, sentence):
        sentence = re.sub(r'\W+', '', sentence)
        return sentence

    # Convert the current text into a dictionary <K, V>
    # k = Formatted sentence
    # V = value|rank of the sentence
    def get_sentences_ranks(self, content):

        # Split the content into sentences
        sentences = self.split_content_to_sentences(content)

        # Calculate the intersection of every two sentences
        n = len(sentences)
        values = [[0 for x in xrange(n)] for x in xrange(n)]
        for i in range(0, n):
            for j in range(0, n):
                values[i][j] = self.sentences_intersection(sentences[i], sentences[j])

        """
            Purpose: Build sentences dictionary
            The score of a sentences is the sum of all its intersection
            The higher the score, the more likely we will use it in the final portion
        """
        sentences_dic = {}
        for i in range(0, n):
            score = 0
            for j in range(0, n):
                if i == j:
                    continue
                score += values[i][j]
            sentences_dic[self.format_sentence(sentences[i])] = score
        return sentences_dic

    # Return the best sentence in a paragraph from the sentences dictionary
    def get_best_sentence(self, paragraph, sentences_dic):

        # Split the paragraph into sentences
        sentences = self.split_content_to_sentences(paragraph)

        # Ignore short paragraphs
        if len(sentences) < 2:
            return ""

        # Get the best sentence according to the sentences dictionary
        # Looks for the highest "score"
        best_sentence = ""
        highScore = 0
        for s in sentences:
            strip_s = self.format_sentence(s)
            if strip_s:
                if sentences_dic[strip_s] > highScore:
                    highScore = sentences_dic[strip_s]
                    best_sentence = s
        return best_sentence

    # Build the summary
    def get_summary(self, content, sentences_dic):

        # Split the content into paragraphs
        paragraphs = self.split_content_to_paragraphs(content)

        # Add title
        summary = []
        #summary.append(title.strip())# Append a copy of the title with the leading & trailing characters removed
        #summary.append("")

        # Append the best sentence from each paragraph to the final summary
        for p in paragraphs:
            sentence = self.get_best_sentence(p, sentences_dic).strip()
            if sentence:
                summary.append(sentence)

        # Returns the paragraph summary
        return ("\n").join(summary)

    # Supposed to encode the text file into unicode format to handle strange characters UTF-8 doesn't know
    def make_unicode(self, content):
        if type(content) != unicode:
            content = content.decode('utf-8')
            return content
        else:
            return input

def main():
    # Asks for filename.txt
    if len(sys.argv) == 1:
        print "Please enter an EULA file."
        sys.exit(-1)
    hfile = open(sys.argv[1], "r")

    # heading and paragraph vars used by the paragrapher object
    new_heading = ''
    para = []

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
        para.append(data[begin:end])

        sections.append(SummaryTool(heading, para))# Assign the heading and paragraph lists to
        index += 1
        new_heading = heading

    # @TODO Find a way to grab what company owns this digital product
    title = """TeamViewer End-User License Agreement"""
    print(title.strip())

    # Create a SummaryTool object
    st = SummaryTool(new_heading, para)

    index = 0
    for p in sections:
        #print "sample text"
        # OK!!!!
        print "-"*25 + p.header + "-"*25    # Prints the current header value
        # NOT OK!!!!
        sentences_dic = st.get_sentences_ranks(para[index])
        summary = st.get_summary(para[index], sentences_dic)
        print summary                       # Prints the simplified paragraph under each heading
        index += 1

if __name__ == '__main__':
    main()
