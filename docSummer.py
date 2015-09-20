# coding=UTF-8
from __future__ import division
import re

class SummaryTool(object):

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
        s1 = set(sent1.split(" "))
        s2 = set(sent2.split(" "))

        # If there is not intersection, just return 0
        if (len(s1) + len(s2)) == 0:
            return 0

        # Normalize  result by average counted words
        return len(s1.intersection(s2)) / ((len(s1) + len(s2)) / 2)

    # Format a sentence - remove all non-alphbetic chars from the sentence
    # We'll use the formatted sentence as a key in our sentences dictionary
    def format_sentence(self, sentence):
        sentence = re.sub(r'\W+', '', sentence)
        return sentence

    # Convert the current text into a dictionary <K, V>
    # k = The formatted sentence
    # V = The value|rank of the sentence
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

    # Return the best sentence in a paragraph
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
    def get_summary(self, title, content, sentences_dic):

        # Split the content into paragraphs
        paragraphs = self.split_content_to_paragraphs(content)

        # Add the title
        summary = []
        summary.append(title.strip())
        summary.append("")

        # Append the best sentence from each paragraph to the final summary
        for p in paragraphs:
            sentence = self.get_best_sentence(p, sentences_dic).strip()
            if sentence:
                summary.append(sentence)

        return ("\n").join(summary)

def main():

    # @TODO Find a way to grab what company owns this digital product
    title = """
    TeamViewer End-User License Agreement
    """

    # @TODO Find a way to loop content through a list and print the summaries underneath the headers
    content = """
    This End-user License Agreement including its Annex (“EULA”) applies to you and TeamViewer GmbH (“TeamViewer” or “We”) for the licensing and use of our software, which includes the TeamViewer software and all versions, features, applications and modules thereto (“Software”). This EULA also covers any associated media, printed materials and electronic documentation that we make available to you (with our Software and “Product”). Future releases of our Product may warrant amendments to this EULA.
    """

    # Create a SummaryTool object
    st = SummaryTool()

    # Build the sentences dictionary
    sentences_dic = st.get_sentences_ranks(content)

    # Build the summary with the sentences dictionary
    summary = st.get_summary(title, content, sentences_dic)

    # Show the original content
    print content

    # Show the new, summarized content
    print summary

if __name__ == '__main__':
    main()
