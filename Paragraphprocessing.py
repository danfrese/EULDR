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
