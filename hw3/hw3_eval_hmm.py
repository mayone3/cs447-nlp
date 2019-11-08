########################################
## CS447 Natural Language Processing  ##
##           Homework 2               ##
##       Julia Hockenmaier            ##
##       juliahmr@illnois.edu         ##
########################################
##
## Part 1:
## Evaluate the output of your bigram HMM POS tagger
##
import os.path
import sys
from operator import itemgetter
from collections import defaultdict

# Unknown word token
UNK = 'UNK'

# Class that stores a word and tag together
class TaggedWord:
    def __init__(self, taggedString):
        parts = taggedString.split('_');
        self.word = parts[0]
        self.tag = parts[1]


# A class for evaluating POS-tagged data
class Eval:
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
    # Reads a labeled data inputFile, and returns a nested list of sentences, where each sentence is a list of TaggedWord objects
    def readLabeledDataRaw(self, inputFile):
        if os.path.isfile(inputFile):
            file = open(inputFile, "r") # open the input file in read-only mode
            sens = [];
            for line in file:
                raw = line.split()
                sentence = []
                for token in raw:
                    sentence.append(token)
                sens.append(sentence) # append this list as an element to the list of sentences
            return sens
        else:
            print("Error: unlabeled data file %s does not exist" % inputFile)  # We should really be throwing an exception here, but for simplicity's sake, this will suffice.
            sys.exit() # exit the script

    ################################
    #intput:                       #
    #    goldFile: string          #
    #    testFile: string          #
    #output: None                  #
    ################################
    def __init__(self, goldFile, testFile):
        print("Your task is to implement an evaluation program for POS tagging")
        self.gold = self.readLabeledData(goldFile)
        self.test = self.readLabeledData(testFile)
        self.goldraw = self.readLabeledDataRaw(goldFile)
        self.testraw = self.readLabeledDataRaw(testFile)
        self.tag2idx = defaultdict(int)
        self.idx2tag = defaultdict(str)
        self.cm = []

        # INIT tag2idx and idx2tag DICTIONARY
        tag_idx = 0
        for sen in self.gold:
            for taggedword in sen:
                if taggedword.tag not in self.tag2idx.keys():
                    self.tag2idx[taggedword.tag] = tag_idx
                    self.idx2tag[tag_idx] = taggedword.tag
                    tag_idx += 1

        # INIT CONFUSION MATRIX
        for i in range(0, len(self.tag2idx)):
            cm_row = []
            for j in range(0, len(self.tag2idx)):
                cm_row.append(0)
            self.cm.append(cm_row)

        if len(self.gold) != len(self.test) or len(self.goldraw) != len(self.testraw):
            print("File size mismatch!")
            print("Gold file size = " + str(len(self.gold)))
            print("Test file size = " + str(len(self.test)))
            sys.exit()

    ################################
    #intput: None                  #
    #output: float                 #
    ################################
    def getTokenAccuracy(self):
        print("Return the percentage of correctly-labeled tokens")
        count = 0.0
        total = 0.0

        for i in range(0, len(self.goldraw)):
            for j in range(0, len(self.goldraw[i])):
                total += 1
                if self.goldraw[i][j] == self.testraw[i][j]:
                    count += 1

        print(str(count) + ' / ' + str(total))
        return count/total

    ################################
    #intput: None                  #
    #output: float                 #
    ################################
    def getSentenceAccuracy(self):
        print("Return the percentage of sentences where every word is correctly labeled")
        count = 0.0
        total = 0.0

        for i in range(0, len(self.goldraw)):
            total += 1.0
            if self.goldraw[i] == self.testraw[i]:
                count += 1.0

        print(str(count) + ' / ' + str(total))
        return count/total

    ################################
    #intput:                       #
    #    outFile: string           #
    #output: None                  #
    ################################
    def writeConfusionMatrix(self, outFile):
        print("Write a confusion matrix to outFile; elements in the matrix can be frequencies (you don't need to normalize)")
        f=open(outFile, 'w+')
        for i in range(0, len(self.test)):
            for j in range(0, len(self.test[i])):
                predicted = self.test[i][j].tag
                actual = self.gold[i][j].tag

                self.cm[self.tag2idx[actual]][self.tag2idx[predicted]] += 1
        # print(self.cm[self.tag2idx['NNP']][self.tag2idx['NNP']])

        # print(self.cm)
        print(self.tag2idx)

        # FIRST ROW
        for i in range(0, len(self.idx2tag)):
            if i != len(self.idx2tag)-1:
                print(self.idx2tag[i], end=',', file=f)
            else:
                print(self.idx2tag[i], end='\n', file=f)

        # OTHER ROWs
        for i in range(0, len(self.idx2tag)):
            # PRINT TAG NAME
            print(self.idx2tag[i], end=',', file=f)
            # PRINT CM ROW
            for j in range(0, len(self.idx2tag)):
                # IF NOT LAST ROW
                if j != len(self.idx2tag)-1:
                    print(self.cm[i][j], end=',', file=f)
                # IF LAST ROW
                else:
                    print(self.cm[i][j], end='\n', file=f)

    ################################
    #intput:                       #
    #    tagTi: string             #
    #output: float                 #
    ################################
    def getPrecision(self, tagTi):
        print("Return the tagger's precision when predicting tag t_i")
        tp = 0.0
        fp = 0.0

        for i in range(0, len(self.test)):
            for j in range(0, len(self.test[i])):
                if self.test[i][j].tag == tagTi:
                    if self.gold[i][j].tag == tagTi:
                        tp += 1.0
                    else:
                        fp += 1.0

        print(str(tp) + ' / ' + str(tp+fp))
        return tp/(tp+fp)

    ################################
    #intput:                       #
    #    tagTi: string             #
    #output: float                 #
    ################################
    # Return the tagger's recall on gold tag t_j
    def getRecall(self, tagTj):
        print("Return the tagger's recall for correctly predicting gold tag t_j")
        tp = 0.0
        fn = 0.0

        for i in range(0, len(self.gold)):
            for j in range(0, len(self.gold[i])):
                if self.gold[i][j].tag == tagTj:
                    if self.test[i][j].tag == tagTj:
                        tp += 1.0
                    else:
                        fn += 1.0

        print(str(tp) + ' / ' + str(tp+fn))
        return tp/(tp+fn)

if __name__ == "__main__":
    # Pass in the gold and test POS-tagged data as arguments
    if len(sys.argv) < 2:
        print("Call hw2_eval_hmm.py with two arguments: gold.txt and out.txt")
    else:
        gold = sys.argv[1]
        test = sys.argv[2]
        # You need to implement the evaluation class
        eval = Eval(gold, test)
        # Calculate accuracy (sentence and token level)
        print("Token accuracy: ", eval.getTokenAccuracy())
        print("Sentence accuracy: ", eval.getSentenceAccuracy())
        # Calculate recall and precision
        print("Precision for tag NNP: ", eval.getPrecision('NNP'))
        print("Recall on tag NNP: ", eval.getRecall('NNP'))
        # Write a confusion matrix
        eval.writeConfusionMatrix("confusion_matrix.txt")
