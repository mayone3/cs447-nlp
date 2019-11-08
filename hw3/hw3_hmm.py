########################################
## CS447 Natural Language Processing  ##
##           Homework 2               ##
##       Julia Hockenmaier            ##
##       juliahmr@illnois.edu         ##
########################################
##
## Part 1:
## Train a bigram HMM for POS tagging
##
import os.path
import sys
from operator import itemgetter
from collections import defaultdict
import math
from math import log

# Unknown word token
UNK = 'UNK'

# Class that stores a word and tag together
class TaggedWord:
    def __init__(self, taggedString):
        parts = taggedString.split('_');
        self.word = parts[0]
        self.tag = parts[1]

# Class definition for a bigram HMM
class HMM:
### Helper file I/O methods ###
    ################################
    #intput:                       #
    #    inputFile: string         #
    #output: list                  #
    ################################
    # Reads a labeled data inputFile, and returns a nested list of sentences, where each sentence is a list of TaggedWord objects
    def readLabeledData(self, inputFile):
        if os.path.isfile(inputFile):
            file = open(inputFile, "r") # open the input file in read-only mode
            sens = [];
            for line in file:
                raw = line.split()
                sentence = []
                for token in raw:
                    sentence.append(TaggedWord(token))
                sens.append(sentence) # append this list as an element to the list of sentences
            return sens
        else:
            print("Error: unlabeled data file %s does not exist" % inputFile)  # We should really be throwing an exception here, but for simplicity's sake, this will suffice.
            sys.exit() # exit the script

    ################################
    #intput:                       #
    #    inputFile: string         #
    #output: list                  #
    ################################
    # Reads an unlabeled data inputFile, and returns a nested list of sentences, where each sentence is a list of strings
    def readUnlabeledData(self, inputFile):
        if os.path.isfile(inputFile):
            file = open(inputFile, "r") # open the input file in read-only mode
            sens = [];
            for line in file:
                sentence = line.split() # split the line into a list of words
                sens.append(sentence) # append this list as an element to the list of sentences
            return sens
        else:
            print("Error: unlabeled data file %s ddoes not exist" % inputFile)  # We should really be throwing an exception here, but for simplicity's sake, this will suffice.
            sys.exit() # exit the script
### End file I/O methods ###

    ################################
    #intput:                       #
    #    unknownWordThreshold: int #
    #output: None                  #
    ################################
    # Constructor
    def __init__(self, unknownWordThreshold=5):
        # Unknown word threshold, default value is 5 (words occuring fewer than 5 times should be treated as UNK)
        self.minFreq = unknownWordThreshold
        ### Initialize the rest of your data structures here ###
        self.word2freq = defaultdict(float)
        self.tag2idx = defaultdict(float)
        self.idx2tag = defaultdict(str)
        self.i = defaultdict(float)
        self.t = defaultdict(lambda: defaultdict(float))
        self.e = defaultdict(lambda: defaultdict(float))

    ################################
    #intput:                       #
    #    trainFile: string         #
    #output: None                  #
    ################################
    # Given labeled corpus in trainFile, build the HMM distributions from the observed counts
    def train(self, trainFile):
        data = self.readLabeledData(trainFile) # data is a nested list of TaggedWords

        # make __word2freq & tag2idx
        __word2freq = defaultdict(float)
        tag_idx = 0
        for sen in data:
            for taggedword in sen:
                __word2freq[taggedword.word] += 1
                if taggedword.tag not in self.tag2idx.keys():
                    self.tag2idx[taggedword.tag] = tag_idx
                    self.idx2tag[tag_idx] = taggedword.tag
                    tag_idx += 1

        # replace with unk and make word2freq
        for k in __word2freq.keys():
            if __word2freq[k] < self.minFreq:
                self.word2freq[UNK] += __word2freq[k]
            else:
                self.word2freq[k] += __word2freq[k]

        i_total = 0.0
        t_total = defaultdict(float)
        e_total = defaultdict(float)
        for sen in data:
            # make initial probability
            self.i[sen[0].tag] += 1.0
            i_total += 1.0

            # make transition probability
            for i in range(1, len(sen)):
                self.t[sen[i-1].tag][sen[i].tag] += 1.0
                t_total[sen[i-1].tag] += 1.0

            # make emission probability
            for taggedword in sen:
                if taggedword.word in self.word2freq.keys():
                    self.e[taggedword.tag][taggedword.word] += 1.0
                    e_total[taggedword.tag] += 1.0
                    # print(taggedword.tag)
                    # print(e_total[taggedword.tag])
                else:
                    self.e[taggedword.tag][UNK] += 1.0
                    e_total[taggedword.tag] += 1.0
                    # print(taggedword.tag)
                    # print(e_total[taggedword.tag])

        # smooth transition probability
        for t_i in self.tag2idx.keys():
            for t_j in self.tag2idx.keys():
                self.t[t_i][t_j] += 1.0
                t_total[t_i] += 1.0

        # normalize self.i, self.t and self.e
        for t_i in self.i.keys():
            self.i[t_i] = self.i[t_i] / i_total

        for t_i in self.t.keys():
            for t_j in self.t.keys():
                self.t[t_i][t_j] = self.t[t_i][t_j] / t_total[t_i]

        for t_i in self.e.keys():
            for w_i in self.e[t_i].keys():
                self.e[t_i][w_i] = self.e[t_i][w_i] / e_total[t_i]

        #print("Your first task is to train a bigram HMM tagger from an input file of POS-tagged text")

    ################################
    #intput:                       #
    #     testFile: string         #
    #    outFile: string           #
    #output: None                  #
    ################################
    # Given an unlabeled corpus in testFile, output the Viterbi tag sequences as a labeled corpus in outFile
    def test(self, testFile, outFile):
        data = self.readUnlabeledData(testFile)
        f=open(outFile, 'w+')
        count = 0
        for sen in data:
            count += 1
            if (count % 100 == 0):
                print("Testing sentence " + str(count))
            vitTags = self.viterbi(sen)
            senString = ''
            for i in range(len(sen)):
                senString += sen[i]+"_"+vitTags[i]+" "
            # print(senString.rstrip(), end="\n")
            print(senString.rstrip(), end="\n", file=f)

    ################################
    #intput:                       #
    #    words: list               #
    #output: list                  #
    ################################
    # Given a list of words, runs the Viterbi algorithm and returns a list containing the sequence of tags
    # that generates the word sequence with highest probability, according to this HMM
    def viterbi(self, words):
        #print("Your second task is to implement the Viterbi algorithm for the HMM tagger")
        # returns the list of Viterbi POS tags (strings)
        n = len(words)
        t = len(self.tag2idx)

        # INITIALIZE TRELLIS and BACKPOINTER MATRIX
        trellis = []
        bp = []
        for i in range(0, t):
            trellis_row = []
            bp_row = []
            # row loop
            for j in range(0, n):
                trellis_row.append(-math.inf)
                bp_row.append(-1)
            trellis.append(trellis_row)
            bp.append(bp_row)

        # FIRST COLUMN
        # print("Calculating column 0")
        for t_i in self.t.keys():
            # EMISSION PROBABILITY
            if self.word2freq[words[0]] >= self.minFreq:
                ep = self.e[t_i][words[0]]
            else:
                ep = self.e[t_i][UNK]
            # PROBABILITY
            try:
                trellis[self.tag2idx[t_i]][0] = log(self.i[t_i]) + log(ep)
            except:
                trellis[self.tag2idx[t_i]][0] = -math.inf
        # print("Finished column 0")

        # OTHER COLUMNS
        for j in range(1, n):
            # print("Calculating column " + str(j))
            for t_i in self.t.keys():
                # EMISSION PROBABILITY
                if self.word2freq[words[j]] >= self.minFreq:
                # if words[j] in self.word2freq.keys():
                    ep = self.e[t_i][words[j]]
                else:
                    ep = self.e[t_i][UNK]

                if ep != 0:
                    # TRANSITION POSSIBILITY
                    pmax = -math.inf
                    kmax = -1
                    for t_k in self.t.keys():
                        tp = self.t[t_k][t_i]
                        try:
                            p = trellis[self.tag2idx[t_k]][j-1] + log(ep) + log(tp)
                        except:
                            p = -math.inf
                        if p > pmax:
                            pmax = p
                            kmax = self.tag2idx[t_k]
                    trellis[self.tag2idx[t_i]][j] = pmax
                    bp[self.tag2idx[t_i]][j] = kmax
            # print("Finished column " + str(j))

        # FIND MAX IN LAST COLUMN
        imax = -1
        pmax = -math.inf
        for i in range(0, t):
            p = trellis[i][n-1]
            if p > pmax:
                pmax = p
                imax = i

        j = n-1
        i = imax
        _tags = []
        _tags.append(self.idx2tag[i])
        while j > 0:
            i = bp[i][j]    # next i
            _tags.append(self.idx2tag[i])
            j -= 1
        _tags.reverse()
        # print("Finished Viterbi")
        return _tags
        # return ["NULL"]*len(words) # this returns a dummy list of "NULL", equal in length to words

if __name__ == "__main__":
    tagger = HMM()
    tagger.train('train.txt')
    print("Finished Training")
    tagger.test('test.txt', 'out.txt')
