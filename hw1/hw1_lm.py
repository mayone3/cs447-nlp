########################################
## CS447 Natural Language Processing  ##
##           Homework 1               ##
##       Julia Hockenmaier            ##
##       juliahmr@illnois.edu         ##
########################################
##
## Part 1:
## Develop a smoothed n-gram language model and evaluate it on a corpus
##
import os.path
import sys
import random
import math
from operator import itemgetter
from collections import defaultdict
#----------------------------------------
#  Data input
#----------------------------------------

# Read a text file into a corpus (list of sentences (which in turn are lists of words))
# (taken from nested section of HW0)
def readFileToCorpus(f):
    """ Reads in the text file f which contains one sentence per line.
    """
    if os.path.isfile(f):
        file = open(f, "r") # open the input file in read-only mode
        i = 0 # this is just a counter to keep track of the sentence numbers
        corpus = [] # this will become a list of sentences
        print("Reading file ", f)
        for line in file:
            i += 1
            sentence = line.split() # split the line into a list of words
            #append this lis as an element to the list of sentences
            corpus.append(sentence)
            if i % 1000 == 0:
        	#print a status message: str(i) turns int i into a string
        	#so we can concatenate it
                sys.stderr.write("Reading sentence " + str(i) + "\n")
            #endif
        #endfor
        return corpus
    else:
    #ideally we would throw an exception here, but this will suffice
        print("Error: corpus file ", f, " does not exist")
        sys.exit() # exit the script
    #endif
#enddef


# Preprocess the corpus to help avoid sess the corpus to help avoid sparsity
def preprocess(corpus):
    #find all the rare words
    freqDict = defaultdict(int)
    for sen in corpus:
	    for word in sen:
	        freqDict[word] += 1
        #endfor
    #endfor

    #replace rare words with unk
    for sen in corpus:
        for i in range(0, len(sen)):
            word = sen[i]
            if freqDict[word] < 2:
                sen[i] = UNK
            #endif
        #endfor
    #endfor

    #bookend the sentences with start and end tokens
    for sen in corpus:
        sen.insert(0, start)
        sen.append(end)
    #endfor

    return corpus
#enddef

def preprocessTest(vocab, corpus):
    #replace test words that were unseen in the training with unk
    for sen in corpus:
        for i in range(0, len(sen)):
            word = sen[i]
            if word not in vocab:
                sen[i] = UNK
            #endif
        #endfor
    #endfor

    #bookend the sentences with start and end tokens
    for sen in corpus:
        sen.insert(0, start)
        sen.append(end)
    #endfor

    return corpus
#enddef

# Constants
UNK = "UNK"     # Unknown word token
start = "<s>"   # Start-of-sentence token
end = "</s>"    # End-of-sentence-token


#--------------------------------------------------------------
# Language models and data structures
#--------------------------------------------------------------

# Parent class for the three language models you need to implement
class LanguageModel:
    # Initialize and train the model (ie, estimate the model's underlying probability
    # distribution from the training corpus)
    def __init__(self, corpus):
        print("""Your task is to implement five kinds of n-gram language models:
      a) an (unsmoothed) unigram model (UnigramModel)
      b) a unigram model smoothed using Laplace smoothing (SmoothedUnigramModel)
      c) an unsmoothed bigram model (BigramModel)
      """)
    #enddef

    # Generate a sentence by drawing words according to the
    # model's probability distribution
    # Note: think about how to set the length of the sentence
    #in a principled way
    def generateSentence(self):
        print("Implement the generateSentence method in each subclass")
        return "mary had a little lamb ."
    #enddef

    # Given a sentence (sen), return the probability of
    # that sentence under the model
    def getSentenceProbability(self, sen):
        print("Implement the getSentenceProbability method in each subclass")
        return 0.0
    #enddef

    # Given a corpus, calculate and return its perplexity
    #(normalized inverse log probability)
    def getCorpusPerplexity(self, corpus):
        print("Implement the getCorpusPerplexity method")
        return 0.0
    #enddef

    # Given a file (filename) and the number of sentences, generate a list
    # of sentences and write each to file along with its model probability.
    # Note: you shouldn't need to change this method
    def generateSentencesToFile(self, numberOfSentences, filename):
        filePointer = open(filename, 'w+')
        for i in range(0,numberOfSentences):
            sen = self.generateSentence()
            prob = self.getSentenceProbability(sen)
            stringGenerated = str(prob) + " " + " ".join(sen)
        #endfor
    #enddef
#endclass

# Unigram language model
class UnigramModel(LanguageModel):
    def __init__(self, corpus):
        print("Initializing unsmoothed unigram model")
        self.counts = defaultdict(float)
        self.total = 0.0
        self.train(corpus)
    #enddef

    # Add observed counts from corpus to the distribution
    def train(self, corpus):
        for sen in corpus:
            for word in sen:
                if word == start:
                    continue
                self.counts[word] += 1.0
                self.total += 1.0
            #endfor
        #endfor
    #enddef

    # Returns the probability of word in the distribution
    def prob(self, word):
        try:
            return self.counts[word]/self.total
        except:
            try:
                return self.counts[UNK]/self.total
            except:
                return 0
    #enddef

    # Generate a single random word according to the distribution
    def draw(self):
        rand = random.random()
        for word in self.counts.keys():
            rand -= self.prob(word)
            if rand <= 0.0:
                return word
            #endif
        #endfor
    #enddef

    # Generate a random sentence by drawing words until EOS drawn
    def generateSentence(self):
        print("Generating sentence for unsmoothed unigram model.")
        word = start
        sen = []
        sen.append(word)

        while (word != end):
            word = self.draw()
            while (word == start):
                word = self.draw()  # drawing <s> is not allowed
            #endwhile
            sen.append(word)
        #endwhile

        return sen
    #enddef

    def getSentenceProbability(self, sen):
        print("Calculating sentence probability for unsmoothed unigram model.")
        prob_log = 0.0
        prob_ret = 0.0

        for word in sen:
            if word == start:
                continue
            #endif
            try:
                prob_log += math.log(self.prob(word))
            except:
                return 0
        #endfor

        prob_ret = math.exp(prob_log)
        return prob_ret
    #enddef

    def getCorpusPerplexity(self, corpus):
        print("Calculating corpus perplexity for unsmoothed unigram model.")
        perp_log = 0.0
        perp_ret = 0.0
        num_words = 0.0

        for sen in corpus:
            for word in sen:
                if word == start:
                    continue
                #endif
                num_words += 1.0
                if self.prob(word) == 0:
                    return math.inf
                else:
                    perp_log += math.log(self.prob(word))
            #endfor
        #endfor

        if (num_words == 0):
            perp_ret = 0
        else:
            perp_ret = math.exp(-perp_log/num_words)
        return perp_ret
    #enddef
#endclass

#Smoothed unigram language model (use laplace for smoothing)
class SmoothedUnigramModel(LanguageModel):
    def __init__(self, corpus):
        print("Initializing smoothed unigram model")
        self.counts = defaultdict(float)
        self.total = 0.0
        self.train(corpus)
        self.smooth()
    #enddef

    # Add observed counts from corpus to the distribution
    def train(self, corpus):
        for sen in corpus:
            for word in sen:
                if word == start:
                    continue
                self.counts[word] += 1.0
                self.total += 1.0
            #endfor
        #endfor
    #enddef

    # Smooth the trained model using laplace
    def smooth(self):
        for word in self.counts:
            self.counts[word] += 1.0
            self.total += 1.0
        #endfor
    #enddef

    # Returns the probability of word in the distribution
    def prob(self, word):
        try:
            return self.counts[word]/self.total
        except:
            # return self.counts[UNK]/self.total
            try:
                return self.counts[UNK]/self.total
            except:
                return 0
    #enddef

    # Generate a single random word according to the distribution
    def draw(self):
        rand = random.random()
        for word in self.counts.keys():
            rand -= self.prob(word)
            if rand <= 0.0:
                return word
            #endif
        #endfor
    #enddef

    def generateSentence(self):
        print("Generating sentence for smoothed unigram model.")
        word = start
        sen = []
        sen.append(word)

        while (word != end):
            word = self.draw()
            while (word == start):
                word = self.draw()  # drawing <s> is not allowed
            #endwhile
            sen.append(word)
        #endwhile

        return sen
    #enddef

    def getSentenceProbability(self, sen):
        print("Calculating sentence probability for smoothed unigram model.")
        prob_log = 0.0
        prob_ret = 0.0

        for word in sen:
            if word == start:
                continue
            #endif
            try:
                prob_log += math.log(self.prob(word))
            except:
                return 0
        #endfor

        prob_ret = math.exp(prob_log)
        return prob_ret
    #enddef

    def getCorpusPerplexity(self, corpus):
        print("Calculating corpus perplexity for smoothed unigram model.")
        # corpus = preprocess(corpus)
        perp_log = 0.0
        perp_ret = 0.0
        num_words = 0.0

        for sen in corpus:
            for word in sen:
                if word == start:
                    continue
                #endif
                num_words += 1.0
                if (self.prob(word) == 0):
                    return math.inf
                else:
                    perp_log +=  math.log(self.prob(word))
            #endfor
        #endfor

        if (num_words == 0):
            perp_ret = 0
        else:
            perp_ret = math.exp(-perp_log/num_words)
        return perp_ret
    #enddef
#endclass

# Unsmoothed bigram language model
class BigramModel(LanguageModel):
    def __init__(self, corpus):
        print("Initializing bigram model")
        self.counts = defaultdict(lambda: defaultdict(float))
        self.total = defaultdict(float)
        self.train(corpus)
    #enddef


    def train(self, corpus):
        for sen in corpus:
            for i in range(1, len(sen)):
                self.counts[sen[i-1]][sen[i]] += 1.0
                self.total[sen[i-1]] += 1.0
            #endfor
        #endfor
    #enddef

    # Returns the probability of word in the distribution
    def prob(self, word1, word2):
        try:
            return self.counts[word1][word2]/self.total[word1]
        except:
            try:
                return self.counts[word1][UNK]/self.total[word1]
            except:
                try:
                    return self.counts[UNK][word2]/self.total[UNK]
                except:
                    try:
                        return self.counts[UNK][UNK]/self.total[UNK]
                    except:
                        return 0
    #enddef

    # Generate a single random word according to the distribution
    def draw(self, word1):
        rand = random.random()
        for word2 in self.counts[word1].keys():
            rand -= self.prob(word1, word2)
            if rand <= 0.0:
                return word2
            #endif
        #endfor
    #enddef

    def generateSentence(self):
        print("Generating sentence for bigram model.")
        word1 = start
        word2 = start
        sen = []
        sen.append(word1)

        while (word2 != end):
            word2 = self.draw(word1)
            while (word2 == start):
                word2 = self.draw(word1)  # drawing <s> is not allowed
            #endwhile
            sen.append(word2)
            word1 = word2
        #endwhile

        return sen
    #enddef

    def getSentenceProbability(self, sen):
        print("Calculating sentence probability for bigram model.")
        prob_log = 0.0
        prob_ret = 0.0

        for i in range(1, len(sen)):
            try:
                prob_log += math.log(self.prob(sen[i-1], sen[i]))
            except:
                return 0    # when prob(sen[i-1], sen[i]) == 0
        #endfor

        prob_ret = math.exp(prob_log)
        return prob_ret
    #enddef

    def getCorpusPerplexity(self, corpus):
        print("Calculating corpus perplexity for bigram model.")
        perp_log = 0.0
        perp_ret = 0.0
        num_bigrams = 0.0

        for sen in corpus:
            for i in range(1, len(sen)):
                num_bigrams += 1.0
                if self.prob(sen[i-1], sen[i]) == 0:
                    return math.inf
                else:
                    perp_log +=  math.log(self.prob(sen[i-1], sen[i]))
            #endfor
        #endfor

        perp_ret = math.exp(-perp_log/num_bigrams)
        return perp_ret
    #enddef
#endclass

# Sample class for a unsmoothed unigram probability distribution
# Note:
#       Feel free to use/re-use/modify this class as necessary for your
#       own code (e.g. converting to log probabilities after training).
#       This class is intended to help you get started
#       with your implementation of the language models above.
class UnigramDist:
    def __init__(self, corpus):
        self.counts = defaultdict(float)
        self.total = 0.0
        self.train(corpus)
    #enddef

    # Add observed counts from corpus to the distribution
    def train(self, corpus):
        for sen in corpus:
            for word in sen:
                if word == start:
                    continue
                self.counts[word] += 1.0
                self.total += 1.0
            #endfor
        #endfor
    #enddef

    # Returns the probability of word in the distribution
    def prob(self, word):
        return self.counts[word]/self.total
    #enddef

    # Generate a single random word according to the distribution
    def draw(self):
        rand = random.random()
        for word in self.counts.keys():
            rand -= self.prob(word)
            if rand <= 0.0:
                return word
            #endif
        #endfor
    #enddef
#endclass

#-------------------------------------------
# The main routine
#-------------------------------------------
if __name__ == "__main__":
    #read your corpora
    trainCorpus = readFileToCorpus('train.txt')
    trainCorpus = preprocess(trainCorpus)

    posTestCorpus = readFileToCorpus('pos_test.txt')
    negTestCorpus = readFileToCorpus('neg_test.txt')

    vocab = set()
    # Please write the code to create the vocab over here before the function preprocessTest
    print("""Task 0: create a vocabulary(collection of word types) for the train corpus""")


    posTestCorpus = preprocessTest(vocab, posTestCorpus)
    negTestCorpus = preprocessTest(vocab, negTestCorpus)

    # Run sample unigram dist code
    unigramDist = UnigramDist(trainCorpus)
    print("Sample UnigramDist output:")
    print("Probability of \"vader\": ", unigramDist.prob("vader"))
    print("Probability of \""+UNK+"\": ", unigramDist.prob(UNK))
    print("\"Random\" draw: ", unigramDist.draw())
