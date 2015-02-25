# -*- coding: cp1252 -*-
#####################IMPORTS###################
from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import random
import codecs
######################IMPORTS/end##############

##########################################################################
##########################################################################
############################                  ############################
######################         INTRODUCTION         ######################
#################                                        #################
#############            Automatic Text Generator            #############
##########                                                      ##########
########      This file contains the class used for,              ########
########      generating a new Automatic Text Generator object.   ########
########      Every part of the code is well commented.           ########
########      I hope you will enjoy reading it.                   ########
##########                                                      ##########
#############            -Kalle Kromann                      #############
#################                                        #################
######################                              ######################
############################                  ############################
##########################################################################
##########################################################################

class AutomaticTextGenerator(object):
    def __init__(self, model = 1):
        """
        args:
        model: Int 1, 2 or 3. Specifies which model to use.
        ---------------------------------------------------------------------------
        Constructs Automatic Text Generator object.

        To use object, following three steps must be taken:
            1. Call method self.defineAlphabet(alphabet) to define which symbols to accept from the text.
            2. Call method self.feedInput(textfile) to feed text.
            3. Call method self.identifyProbabilities() to perform various statistical calculations.

        Call self.changeModel(newModel) to change model.

        You can now generate a text with self.generateText(N)

        Description of models
        Model 1:
            Generates text of previously independent symbols.
        Model 2:
            Generates text of previously dependent pairs of symbols.
        Model 3:
            Generates text of previously dependent words.
        """
        self.textFile = None
        self.alphabet = {}
        self.cleanAlphabet = {}
        self.pairs = {}
        self.words = {}
        self.wordPairs = {}
        self.text = ""
        self.cleanText = ""
        self.newtext = ""
        self.normSymbols = {}
        self.normPairs = {}
        self.normWords = {}
        self.normWordPairs = {}
        self.validTransformations = {}
        self.pairTableArray = None
        self.wordPairTableArray = None
        self.validWordTransformations = {}
        self.symbolCount = 0
        self.defined = False
        self.fed = False
        self.identified = False
        if 4 > model > 0:
            self.model = model
        else:
            raise ValueError("model must be int 1, 2 or 3")

    def changeModel(self, model):
        """
        args:
        model: Int 1, 2 or 3. Specifies which model to change to.
        ---------------------------------------------------------------------------
        Changes model used for generating text. See model description in self.__init__ docstring.
        If object has not yet been initialized for the new model the methods,
        self.feedInput(file) (with same textfile) and self.identifyProbabilities() are called again.
        """

        if 0 < model < 4:
            self.model = model
        else:
            raise ValueError("model must be int 1, 2 or 3")

        if self.model == 1 and len(self.normSymbols) == 0:
            self.feedInput(self.textFile, True)
            self.identifyProbabilities(True)
        elif self.model == 2 and len(self.normPairs) == 0:
            self.feedInput(self.textFile, True)
            self.identifyProbabilities(True)
        elif self.model == 3 and len(self.normWordPairs) == 0:
            self.feedInput(self.textFile, True)
            self.identifyProbabilities(True)

    def defineAlphabet(self, alphabet, language="Danish"):
        """
        args:
        alphabet: Text file ('name.txt') containing symbols to accept from file, and use to generate text.
                * All non-letter symbols must be at the end of the file. (So letters first, then non-letters)
                * The code will not raise errors if using another syntax, but results may be faulty.
                * File must be UTF-8 encoded.
        language: Determines how many letter-symbols are in alphabet.
                * Defaults to "Danish".
                * Supported languages are: "Danish", "English"
                * If language is "Danish" there are 58 letter-symbols. (upper- and lowercase)
                * If language is "English" there are 54 letter-symbols. (upper- and lowercase)
        ---------------------------------------------------------------------------
        Defines which symbols are valid symbols for the text generation.

        Creates keys in self.alphabet for every element in text file.
        Creates keys in self.cleanAlphabet for every letter-symbol in text file.
        """
        if self.defined:
            self.alphabet = {}
            self.cleanAlphabet = {}
        self.defined = True
        # Checks which language is used, and stores number of letter-symbols in numLetters.
        if language == "Danish":
            numLetters = 58
        elif language == "English":
            numLetters = 54
        else:
            raise ValueError("Language is not supported")

        with codecs.open(alphabet, 'r', encoding="UTF-8") as alph:
            n = 0
            for line in alph:
                for i in line:
                    # Create keys in self.alphabet for each symbol.
                    self.alphabet[i] = 0
                    # Also create keys in self.cleanAlphabet for each letter-symbol.
                    # If language argument is left out, danish is assumed (so there are 29 letters)
                    if n < numLetters + 1:
                        self.cleanAlphabet[i] = 0
                    n += 1
        # Delete unwanted symbol. (BOM)
        del self.alphabet[u'\ufeff']
        del self.cleanAlphabet[u'\ufeff']
        # Tests
        if __debug__:
            print "~"*80
            print "Tests for defineAlphabet method:"
            print "Length of alphabet is".format(len(self.alphabet)), len(self.alphabet)
            print "Length of cleanAlphabet({0}) is same as numLetters,".format(len(self.cleanAlphabet)), \
                len(self.cleanAlphabet) == numLetters
            flag = True
            for key in self.cleanAlphabet:
                if key in self.alphabet:
                    continue
                else:
                    flag = False
            if flag:
                print "The keys of self.cleanAlphabet are all in self.alphabet, True"
            elif not flag:
                print "The keys of self.cleanAlphabet are all in self.alphabet, False"

    def feedInput(self, textfile, sameFile=False):
        """
        args:
        textfile: Text file ('name.txt') containing the text you want to use for generating new text.
                    File must be UTF-8 encoded.
        sameFile: Optional argument if user wants to use same file as last file.
        ---------------------------------------------------------------------------
        Feeds text to object. The specified text generation model determines some of the functionality of this method.

        Important functionality:
            ----SHARED----
            - Adds all text to variable self.text. (Only valid symbols)
            - Also adds all text to variable self.cleanText. This text does not contain comma and period.
            - Counts up all occurrences of symbols in text.
                * The number of occurrences are saved as values to the symbols(keys) in self.alphabet.
            - Finds count of symbols in self.text, saves in self.symbolCount.

            ----ONLY MODEL 2----
            - Creates keys in self.pairs for every pair of valid symbols in text.
            - Counts up all occurrences of pairs in text.
                * The number of occurrences are saved as values to the symbols(keys) in self.pairs.

            ----ONLY MODEL 3----
            - Creates keys in self.words for every word in cleanText.
            - Counts up all occurrences of words in text.
                * The number of occurrences are saved as values to the symbols(keys) in self.words.
            - Creates keys in self.wordPairs for every pair of words in cleanText.
            - Counts up all occurrences of word pairs in text.
                * The number of occurrences are saved as values to the symbols(keys) in self.wordPairs.
        """
        if not self.defined:
            raise ValueError("You have not defined an alphabet for this object.")
        # If object has already been fed, reset values.
        if self.fed and not sameFile:
            self.text = ""
            self.cleanText = ""
            for key in self.alphabet:
                self.alphabet[key] = 0
            self.pairs = {}
            self.words = {}
            self.wordPairs = {}
            self.validTransformations = {}
            self.validWordTransformations = {}
        self.fed = True
        self.textFile = textfile
        if not sameFile:
            with codecs.open(textfile, 'r', encoding="UTF-8") as textfile:
                for line in textfile:
                    for i in line:
                        if i in self.alphabet:
                            # Add elements to self.text if elements are valid symbols.
                            self.text += i
                            # Count up occurrences of symbols.
                            self.alphabet[i] += 1
                        if i in self.cleanAlphabet:
                            # Add elements to self.cleanText if elements are valid symbols except comma and period.
                            self.cleanText += i
                        elif i not in self.cleanAlphabet:
                            # If element is comma or period add space to self.cleanText.
                            self.cleanText += " "
            # Find count of symbols
            self.symbolCount = len(self.text)
        for i in self.alphabet:
            if i not in self.validTransformations:
                # Create a key in self.validTransformation for each symbol.
                self.validTransformations[i] = []
        # Create keys for self.pairs if model is 2
        if self.model == 2:
            # Create empty string, splitText, and append all elements from self.text separated by '-'
            splitText = ""
            for i in self.text:
                splitText += i + "-"
            # Create list, symbolList, of all elements between '-' in splitText
            symbolList = splitText.split('-')
            # For every symbol create or count up key in self.pairs. Key is 'symbol + next symbol'
            for j, i in enumerate(symbolList):
                if j < len(symbolList)-1:
                    a, b = symbolList[j], symbolList[j+1]
                    newPair = (a + b)
                    if newPair not in self.pairs:
                        self.pairs[newPair] = 0
                    else:
                        self.pairs[newPair] += 1
        # Create keys for self.words and self.wordPairs if model is 3.
        if self.model == 3:
            # Create list, wordList, of all words in self.cleanText.
            # Create or count up key in self.words for each word in wordList
            wordList = self.cleanText.split()
            for word in wordList:
                if word not in self.words:
                    self.words[word] = 1
                    # Create a key in self.validWordTransformation for each word.
                    self.validWordTransformations[word] = []
                else:
                    self.words[word] += 1
            # For every word create or count up key in self.wordPairs. Key is 'word + next word'
            n = 0
            for j, i in enumerate(wordList):
                if j < len(wordList)-1:
                    newWordPair = (wordList[j], wordList[j+1])
                    if newWordPair not in self.wordPairs:
                        self.wordPairs[newWordPair] = 1
                    else:
                        self.wordPairs[newWordPair] += 1
        # Tests
        if __debug__:
            print "~"*80
            print "Tests for feedInput method:"
            print "The sum of all values in self.alphabet({0})" \
                  " is equal to count of symbols,".format(sum(self.alphabet.values())), \
                sum(self.alphabet.values()) == self.symbolCount
            print "The length of self.validTransformation({0})" \
                  " is equal to the length of self.alphabet,".format(len(self.validTransformations)), \
                len(self.validTransformations) == len(self.alphabet)
            if self.model == 3:
                print "The sum of all values in self.words({0})" \
                      " is equal to count of words,".format(sum(self.words.values())),\
                    sum(self.words.values()) == len(wordList)
                print "The length of self.validWordTransformation({0})" \
                      " is equal to the length of self.words,".format(len(self.validWordTransformations)), \
                    len(self.validWordTransformations) == len(self.words)

    def identifyProbabilities(self, sameFile=False):
        """
        args:
        sameFile: Optional argument if user wants to use same file as last file.
        ---------------------------------------------------------------------------
        This method handles the statistical calculations.
        The calculations are based on which text generation model the object is set to. (1, 2 or 3)
        Nothing is shared between models in this method.

        Important functionality:
            ----ONLY MODEL 1----
            - Creates keys in self.normSymbols for each key(symbol) in self.alphabet.
                * Values of keys(symbols) in self.normSymbols are normalized values of occurrences of that symbol.
            ----ONLY MODEL 2----
            - Creates keys in self.normPairs for each key(symbol-pair) in self.pairs.
                * Values of keys(pairs) in self.normPairs are normalized values of occurrences of that symbol-pair.
            - Creates a numpy array, pairTableArray, consisting the transformation-probabilities for each symbol.
                * self.validTransformations contains same information, but in a dictionary.
            ----ONLY MODEL 3----
            - Creates keys in self.normWordPairs for each key(word-pair) in self.wordPairs.
                * Values of keys(pairs) in self.normWordPairs are normalized values of occurrences of that word-pair.
            - Creates a numpy array, wordPairTableArray, consisting the transformation-probabilities for each word.
                * self.validWordTransformations contains same information, but in a dictionary.
        """
        if not self.defined:
            raise ValueError("You have not defined an alphabet for this object.")
        if not self.fed:
            raise ValueError("You have not fed any input to this object.")
        if self.identified and not sameFile:
            self.normSymbols = {}
            self.normPairs = {}
            self.normWordPairs = {}
            self.pairTableArray = None
            self.wordPairTableArray = None
        self.identified = True
        if self.model == 1:
            for key in self.alphabet:
                # Create keys in self.normSymbols for each key(symbol) in self.alphabet.
                self.normSymbols[key] = self.alphabet[key] / self.symbolCount
            if __debug__:
                print "~"*80
                print "Tests for identifyProbabilities method:"
                flag = True
                for key in self.alphabet:
                    if key in self.normSymbols:
                        continue
                    else:
                        flag = False
                if flag:
                    print "The keys of alphabet are all in normSymbols, True"
                elif not flag:
                    print "The keys of alphabet are all in normSymbols, False"

                print "The values of self.normSymbols accumulate to 1.0,", \
                    0.9999 < sum(self.normSymbols.values()) <= 1.0001
        elif self.model == 2:
            # Calculate normalization factor.
            normFact = sum(self.pairs.values())
            for key in self.pairs:
                # Create keys in self.normPairs for each key(symbol-pair) in self.pairs.
                self.normPairs[key] = self.pairs[key] / normFact
            for i in self.alphabet:
                validNextSymbols = {}
                for key in self.normPairs:
                    if key[0] == i and self.pairs[key] > 0:
                        # For each symbol in alphabet:
                        # Create keys in temporary dictionary, validNextSymbols.
                        # Keys are pairs of symbols, which first symbol is the same as the symbol from alphabet.
                        validNextSymbols[key] = self.normPairs[key]
                # Calculate normalization factor for validNextSymbols.
                normFact = sum(validNextSymbols.values())
                for j in self.alphabet:
                    pair = i + j
                    if pair in validNextSymbols:
                        # Append normalized values of validNextSymbols to the dict self.validTransformations.
                        self.validTransformations[i].append(validNextSymbols[pair] / normFact)
                    else:
                        # Also append values of rest of the pairs to maintain order in self.validTransformations.
                        self.validTransformations[i].append(0.0)
            # Create array, self.pairTableArray containing same information as self.validTransformations. Used to plot.
            symbolPairTable = []
            for i in self.validTransformations:
                symbolPairTable.append(self.validTransformations[i])
            # Delete unwanted empty list. (Mysterious extra symbol)
            del symbolPairTable[-1]
            self.pairTableArray = np.array(symbolPairTable)
            if __debug__:
                print "~"*80
                print "Tests for identifyProbabilities method:"
                flag = True
                for i in self.pairs:
                    if i in self.normPairs:
                        continue
                    else:
                        flag = False
                if flag:
                    print "All symbol-pairs are in self.normPairs, True"
                elif not flag:
                    print "All symbol-pairs are in self.normPairs, False"
                print "The values of self.normPairs accumulate to 1.0,", \
                    0.9999 < sum(self.normPairs.values()) <= 1.0001
                flag = True
                for i in self.alphabet:
                    vals = self.validTransformations[i]
                    if sum(vals) > 0:
                        if 0.9999 < sum(vals) <= 1.0001:
                            continue
                        else:
                            flag = False
                    else:
                        continue
                if flag:
                    print "All valid values of self.validTransformations accumulate to 1.0, True"
                elif not flag:
                    print "All valid values of self.validTransformations accumulate to 1.0, False"

        elif self.model == 3:
            for key in self.words:
                self.normWords[key] = self.words[key] / len(self.words)
            # Calculate normalization factor.
            normFact = sum(self.wordPairs.values())
            for key in self.wordPairs:
                # Create keys in self.normWordPairs for each key(word-pair) in self.wordPairs.
                self.normWordPairs[key] = self.wordPairs[key] / normFact
            n = 0
            for i in self.words:
                validNextWords = {}
                for key in self.normWordPairs:
                    if key[0] == i and self.wordPairs[key] > 0:
                        # For each word in self.words:
                        # Create keys in temporary dictionary, validNextWords.
                        # Keys are pairs of words, which first word is the same as the word from self.words.
                        validNextWords[key] = self.normWordPairs[key]
                # Calculate normalization factor for validNextWords.
                normFact = sum(validNextWords.values())
                for j in self.words:
                    wordPair = (i, j)
                    if wordPair in validNextWords:
                        # Append normalized values of validNextWords to the dict self.validWordTransformations.
                        self.validWordTransformations[i].append(validNextWords[wordPair] / normFact)
                    else:
                        # Also append values of rest of the pairs to maintain order in self.validWordTransformations.
                        self.validWordTransformations[i].append(0.0)
            # Create array, self.wordPairTableArray containing same information as self.validWordTransformations.
            # Used to plot.
            wordPairTable = []
            for i in self.validWordTransformations:
                wordPairTable.append(self.validWordTransformations[i])
            self.wordPairTableArray = np.array(wordPairTable)
            if __debug__:
                print "~"*80
                print "Tests for identifyProbabilities method:"
                flag = True
                for i in self.wordPairs:
                    if i in self.normWordPairs:
                        continue
                    else:
                        flag = False
                if flag:
                    print "All word-pairs are in self.normWordPairs, True"
                elif not flag:
                    print "All word-pairs are in self.normWordPairs, False"
                print "The values of self.normWordPairs accumulate to 1.0,", \
                    0.9999 < sum(self.normWordPairs.values()) <= 1.0001
                flag = True
                for i in self.words:
                    vals = self.validWordTransformations[i]
                    if sum(vals) > 0:
                        if 0.9999 < sum(vals) <= 1.0001:
                            continue
                        else:
                            flag = False
                    else:
                        continue
                if flag:
                    print "All valid values of self.validWordTransformations accumulate to 1.0, True"
                elif not flag:
                    print "All valid values of self.validWordTransformations accumulate to 1.0, False"

    def generateText(self, N):
        """
        args:
        N: Amount of symbols, pairs or word-pairs to generate.
        ---------------------------------------------------------------------------
        Generate a new text by using one of the three text generating models.

        Inner functions:
            -f- isEqual(list)
                |Checks if every element in list is equal
            -f- getSymbol()
                |Find initial symbol
                |Model 1 only uses this method, because the symbols are independent from previous symbols.
                |getSymbol() returns string if model = 1 or 2, and returns tuple if model = 3
            -f- getNextSymbol(prevSymbol)
                |Find all probable symbols (pairs or words) dependent on argument prevSymbol.
                |Not used by model 1
        """
        if not self.defined:
            raise ValueError("You have not defined an alphabet for this object.")
        if not self.fed:
            raise ValueError("You have not fed any input to this object.")
        if not self.identified:
            raise ValueError("You have not identified the probabilities for this data.")
        if N <= 1:
            raise ValueError("N must a positive integer over 0")

        def isEqual(list):
            """
            --INNER FUNCTION--
            args:
            list: List to check
            return:
            True: if elements in list are equal.
            False: if elements in list are not equal.
            ---------------------------------------------------------------------------
            Checks if elements in list are equal
            """
            # Compare all elements in list to first element.
            if len(list) > 0:
                comparer = list[0]
                for i in list:
                    if i != comparer:
                        return False
                return True
            else:
                return True

        def getSymbol():
            """
            --INNER FUNCTION--
            ---------------------------------------------------------------------------
            Get symbol independent of previous symbol.
            """
            valList = []
            # Append values from self.normSymbols if model = 1.
            if self.model == 1:
                for key in self.normSymbols:
                    valList.append(self.normSymbols[key])
                # Tests
                if __debug__:
                    if len(valList) != len(self.normSymbols):
                        print "~"*80
                        print "Error in getSymbol()"
                        print "Length of valList({0}) is equal to length of normSymbols({1}), False".format(
                            len(valList), len(self.normSymbols))
            # Append values from self.normPairs if model = 2.
            elif self.model == 2:
                for key in self.normPairs:
                    valList.append(self.normPairs[key])
                # Tests
                if __debug__:
                    if len(valList) != len(self.normPairs):
                        print "~"*80
                        print "Error in getSymbol()"
                        print "Length of valList({0}) is equal to length of normPairs({1}), False".format(
                            len(valList), len(self.normPairs))
            # Append values from self.normWordPairs if model = 3.
            elif self.model == 3:
                for key in self.normWordPairs:
                    valList.append(self.normWordPairs[key])
                # Tests
                if __debug__:
                    if len(valList) != len(self.normWordPairs):
                        print "~"*80
                        print "Error in getSymbol()"
                        print "Length of valList({0}) is equal to length of normWordPairs({1}), False".format(
                            len(valList), len(self.normWordPairs))
            # Shared code for all models
            # Sort values
            valList.sort()
            accSum, sumChain = 0, []
            # Create list, sumChain, containing elements of accumulated values before that element.
            # We're interested in the intervals between the elements.
            for i in range(len(valList)):
                sumChain.append(accSum)
                accSum += valList[i]
            # Tests
            if __debug__:
                if len(sumChain) != len(valList):
                    print "~"*80
                    print "Error in getSymbol()"
                    print "Length of valList({0}) is equal to length of sumChain({1}), False".format(
                        len(valList), len(sumChain))
            # Generate random float between 0 and 1 and store in variable z.
            z, k, val = random.random(), 0, 0
            symbol = ""
            for i in sumChain:
                if i <= z:
                    # Save/overwrite value from index k in valList if element in sumChain is smaller than z.
                    # This works because index in valList is the same as the index of sumChain.
                    val = valList[k]
                k += 1
            # If model is 1
            # Return the symbol from self.normSymbols that has the same value as previously found value(val).
            if self.model == 1:
                for key in self.normSymbols:
                    if val == self.normSymbols[key]:
                        symbol = key
                # Tests
                if __debug__:
                    if type(symbol) != unicode or len(symbol) != 1:
                        print "~"*80
                        print "Error in getSymbol()"
                        print "Symbol is not of correct format."
                return symbol
            # If model is 2
            # Return the symbol-pair from self.normPairs that has the same value as previously found value(val).
            if self.model == 2:
                for key in self.normPairs:
                    if val == self.normPairs[key]:
                        symbol = key
                # Tests
                if __debug__:
                    if type(symbol) != unicode or len(symbol) != 2:
                        print "~"*80
                        print "Error in getSymbol()"
                        print "Symbol is not of correct format."
                return symbol
            # If model is 3
            # Return the word-pair from self.normWordPairs that has the same value as previously found value(val).
            if self.model == 3:
                for key in self.normWordPairs:
                    if val == self.normWordPairs[key]:
                        symbol = key
                # Tests
                if __debug__:
                    if type(symbol) != tuple or len(symbol) != 2:
                        print "~"*80
                        print "Error in getSymbol()"
                        print "Symbol is not of correct format."
                return symbol

        def getNextSymbol(prevSym):
            """
            --INNER FUNCTION--
            args:
            symbol: Previous symbol
            ---------------------------------------------------------------------------
            Get symbol dependent of last symbol.
            Not used by model 1.
            """
            valList = []
            transDict = {}
            # If model is 2
            if self.model == 2:
                transformations = None
                for i in self.validTransformations:
                    if i == prevSym:
                        # Find transformation-probability array for previous symbol.
                        transformations = self.validTransformations[i]
                n = 0
                for key in self.alphabet:
                    # Create keys in temporary dictionary transDict.
                    # Key is symbol from alphabet. Value is that symbols probability from transformations array.
                    # This works because index in transformations array matches keys in alphabet.
                    transDict[key] = transformations[n]
                    n += 1
                # Tests
                if __debug__:
                    if len(transDict) != len(self.alphabet):
                        print "~"*80
                        print "Error in getNextSymbol()"
                        print "Length of transDict is not equal to length of self.alphabet."
            # If model is 3
            if self.model == 3:
                transformations = None
                for i in self.validWordTransformations:
                    if i == prevSym:
                        # Find transformation-probability array for previous word.
                        transformations = self.validWordTransformations[i]
                n = 0
                for key in self.words:
                    # Create keys in temporary dictionary transDict.
                    # Key is word from self.words. Value is that words probability from transformations array.
                    # This works because index in transformations array matches keys in self.words.
                    transDict[key] = transformations[n]
                    n += 1
                # Tests
                if __debug__:
                    if len(transDict) != len(self.words):
                        print "~"*80
                        print "Error in getNextSymbol()"
                        print "Length of transDict is not equal to length of self.words."

            # Shared code for all models.
            # Append all values to valList from transDict if that value is greater than 0.
            for key in transDict:
                if transDict[key] > 0:
                    valList.append(transDict[key])
            # Sort valList
            valList.sort()
            # Create list, sumChain, containing elements of accumulated values before that element.
            # We're interested in the intervals between the elements.
            accSum, sumChain = 0, []
            for i in range(len(valList)):
                sumChain.append(accSum)
                accSum += valList[i]
            # Tests
            if __debug__:
                if len(sumChain) != len(valList):
                    print "~"*80
                    print "Error in getNextSymbol()"
                    print "Length of valList({0}) is not equal to length of sumChain({1})".format(
                        len(valList), len(sumChain))
            # Generate random float between 0 and 1 and store in variable z.
            z, k, val = random.random(), 0, 0
            symbol = ""
            for i in sumChain:
                if i <= z:
                    # Save/overwrite value from index k in valList if element in sumChain is smaller than z.
                    # This works because index in valList is the same as the index of sumChain.
                    val = valList[k]
                k += 1
            # If model is 2
            # Return the symbol-pair from transDict that has the same value as previously found value(val).
            # If values in valList are equal pick random key from transDict using random module.
            if self.model == 2:
                if not isEqual(valList):
                    for key in transDict:
                        if val == transDict[key]:
                            symbol = prevSym + key
                            # Tests
                            if __debug__:
                                if type(symbol) != unicode or len(symbol) != 2:
                                    print "~"*80
                                    print "Error in getNextSymbol()"
                                    print "Symbol is not of correct format."
                    return symbol
                else:
                    validKeys = []
                    for key in transDict:
                        if transDict[key] > 0:
                            validKeys.append(key)
                    key = random.choice(validKeys)
                    symbol = prevSym + key
                    # Tests
                    if __debug__:
                        if type(symbol) != unicode or len(symbol) != 2:
                            print "~"*80
                            print "Error in getNextSymbol()"
                            print "Symbol is not of correct format."
                    return symbol
            # If model is 3
            # Return the word-pair from transDict that has the same value as previously found value(val).
            # If values in valList are equal pick random key from transDict using random module.
            elif self.model == 3:
                if not isEqual(valList):
                    for key in transDict:
                        if val == transDict[key]:
                            symbol = (prevSym, key)
                            # Tests
                            if __debug__:
                                if type(symbol) != tuple or len(symbol) != 2:
                                    print "~"*80
                                    print "Error in getNextSymbol()"
                                    print "Symbol is not of correct format."
                    return symbol
                else:
                    validKeys = []
                    for key in transDict:
                        if transDict[key] > 0:
                            validKeys.append(key)
                    key = random.choice(validKeys)
                    symbol = (prevSym, key)
                    # Tests
                    if __debug__:
                        if type(symbol) != tuple or len(symbol) != 2:
                            print "~"*80
                            print "Error in getNextSymbol()"
                            print "Symbol is not of correct format."
                    return symbol
        #########################################################################################
        # Following code generates N symbols using either one of the 3 text generation models.  #
        #########################################################################################
        #
        # Clear self.newtext
        self.newtext = ""
        # If model is 1
        # Only call getSymbol() to generate new symbols
        if self.model == 1:
            for i in range(N):
                self.newtext += getSymbol()
            # Tests
            if __debug__:
                print "~"*80
                print "Tests for generated text:"
                print "Number of symbols in self.newtext is equal to N({0}),".format(N), len(self.newtext) == N
        # If model is 2
        # Call getSymbol() to find first symbol. Then call getNextSymbol(first symbol) to find second symbol.
        # Call getNextSymbol(previous symbols) N-2 times.
        if self.model == 2:
            firstPair = getSymbol()
            self.newtext += firstPair[0]
            nextPair = getNextSymbol(firstPair[1])
            self.newtext += nextPair[0]
            lastPair = nextPair
            # Tests
            if __debug__:
                if firstPair[1] != nextPair[0]:
                    print "~"*80
                    print "Tests for generated text:"
                    print "Error. firstPair[1]('{0}') does not match nextPair[0]('{1}').".format(
                        firstPair[1], nextPair[0])
                    if firstPair[1] + nextPair[1] not in self.pairs:
                        print "Error. Pair ({0}) does not exist.".format(lastPair[1] + nextPair[1])
            for i in range(N-2):
                nextPair = getNextSymbol(lastPair[1])
                self.newtext += nextPair[0]
                # Tests
                if __debug__:
                    if lastPair[1] != nextPair[0]:
                        print "~"*80
                        print "Error. lastPair[1]('{0}') does not match nextPair[0]('{1}').".format(
                            lastPair[1], nextPair[0])
                    if lastPair[1] + nextPair[1] not in self.pairs:
                        print "Error. Pair ({0}) does not exist.".format(lastPair[1] + nextPair[1])
                # nextPair now stored in last pair
                lastPair = nextPair
            if __debug__:
                print "~"*80
                print "Tests for generated text:"
                print "Number of symbols in self.newtext is equal to N({0}),".format(N), len(self.newtext) == N
        # If model is 3
        # Call getSymbol() to find first word. Then call getNextSymbol(first word) to find second word.
        # Call getNextSymbol(previous word) N-2 times, to find the following words.
        if self.model == 3:
            firstPair = getSymbol()
            self.newtext += firstPair[0] + " "
            nextPair = getNextSymbol(firstPair[1])
            self.newtext += nextPair[0] + " "
            lastPair = nextPair
            # Tests
            if __debug__:
                if firstPair[1] != nextPair[0]:
                    print "~"*80
                    print "Tests for generated text:"
                    print "Error. firstPair[1]('{0}') does not match nextPair[0]('{1}').".format(
                        firstPair[1], nextPair[0])
            for i in range(N-2):
                nextPair = getNextSymbol(lastPair[1])
                self.newtext += nextPair[0] + " "
                # Tests
                if __debug__:
                    if lastPair[1] != nextPair[0]:
                        print "~"*80
                        print "Tests for generated text:"
                        print "Error. lastPair[1]('{0}') does not match nextPair[0]('{1}').".format(
                            lastPair[1], nextPair[0])
                    if (lastPair[1], nextPair[1]) not in self.wordPairs:
                        print "Error. Pair ({0}) does not exist.".format((lastPair[1], nextPair[1]))
                # nextPair now stored in last pair
                lastPair = nextPair
            if __debug__:
                newTextList = self.newtext.split()
                print "~"*80
                print "Tests for generated text:"
                print "Number of words in self.newtext is equal to N({0}),".format(N), len(newTextList) == N
    def saveText(self, name):
        """
        args:
        name: Filename
            * Filename should not end in .txt, it is added automatically.
        ---------------------------------------------------------------------------
        Saves the text stored in self.newtext generated by self.generateText().
        """
        if len(self.newtext) == 0:
            raise ValueError("You have not generated a new text using this object yet.")
        filename = "{0}(model{1}).txt".format(name, self.model)
        with codecs.open(filename, 'w', encoding='UTF-8') as newFile:
            newFile.write(self.newtext)

    def visualizeData(self, model, show=0, save=0):
        """
        args:
        model: Which model data to plot. You will get error message if model is not initialized.
        show: 0 to not show plots, 1 to show plots. (Defaults to 0)
        save: 0 to not save plot, 1 to save plot. (Defaults to 0)
        ---------------------------------------------------------------------------
        Arranges data to make them more visually accessible.
        Visualize data based on model chosen.
        """
        if not self.defined:
            raise ValueError("You have not defined an alphabet for this object.")
        if not self.fed:
            raise ValueError("You have not fed any input to this object.")
        if not self.identified:
            raise ValueError("You have not identified the probabilities for this data.")

        if model == 1:
            if len(self.normSymbols) > 0:
                # Arrange data
                sortedKeys = []
                sortedVals = []
                takenVals = []
                # Append from normSymbols, all keys to sortedKeys, and all values to sortedVals.
                for key, val in self.normSymbols.iteritems():
                    sortedKeys.append(key)
                    if val not in takenVals:
                        sortedVals.append(val)
                        takenVals.append(val)
                # Sort the lists, then find the corresponding keys or values in normSymbols,
                # and replace list elements with both key and val.
                sortedKeys.sort()
                sortedVals.sort()
                for j, i in enumerate(sortedKeys):
                    if i in self.normSymbols:
                        sortedKeys[j] = (i, self.normSymbols[i])
                for j, i in enumerate(sortedVals):
                    for key in self.normSymbols:
                        if self.normSymbols[key] == i:
                            sortedVals[j] = (key, i)
                # Zip the sorted lists.
                keyX, keyY = zip(*sortedKeys)
                valX, valY = zip(*sortedVals)

                # Define x-axes
                keyXaxes = np.arange(len(keyX))
                valXaxes = np.arange(len(valX))

                # Create first plot. This plot is a histogram for sortedKeys (Symbols).
                fig1 = plt.figure(1)
                plt.title('Symbols arranged alphabetically.')
                ax = fig1.gca()
                ax.bar(keyXaxes + 0.6, keyY)
                ax.set_xticks(keyXaxes + 1)
                ax.set_xticklabels(keyX)
                ax.set_xlabel('Symbols')
                ax.set_ylabel('Number of occurrences (Normalized)')
                ax.set_xlim(0.0, keyXaxes.max() + 2)
                if save == 1:
                    # Save plots
                    plt.savefig('model1Plot1.png')

                # Create second plot. This plot is a histogram for sortedVals (Symbols).
                fig2 = plt.figure(2)
                plt.title('Symbols arranged by ascending values. (Doubles only represented once)')
                ax = fig2.gca()
                ax.bar(valXaxes + 0.6, valY)
                ax.set_xticks(valXaxes + 1)
                ax.set_xticklabels(valX)
                ax.set_xlabel('Symbols')
                ax.set_ylabel('Number of occurrences (Normalized)')
                ax.set_xlim(0.0, valXaxes.max() + 2)
                if save == 1:
                    # Save plots
                    plt.savefig('model1Plot2.png')

                if show == 1:
                    # Show plots
                    plt.show()
                elif show == 0:
                    pass
                else:
                    print "Argument show must be 0 or 1."
                if save == 0:
                    pass
                elif save != 1:
                    print "Argument save must be 0 or 1."
            else:
                print "The model selected has not yet been initialized for this object."
        elif model == 2:
            if len(self.normPairs) > 0:
                sortedVals = []
                takenVals = []
                # Append from normPairs, all values to sortedVals.
                for key, val in self.normPairs.iteritems():
                    if val not in takenVals:
                        sortedVals.append(val)
                        takenVals.append(val)
                # Sort the list, then find the corresponding keys in normPairs,
                # and replace list elements with both key and val.
                sortedVals.sort()
                for j, i in enumerate(sortedVals):
                    for key in self.normPairs:
                        if self.normPairs[key] == i:
                            sortedVals[j] = (key, i)
                # Create list with (key, val) elements for scrambled data plot.
                scrambledData = []
                for key, val in self.normPairs.iteritems():
                    scrambledData.append((key, val))
                # Zip the sorted list and the scrambled list.
                sX, sY = zip(*scrambledData)
                valX, valY = zip(*sortedVals)
                # Define x-axes
                sXaxes = np.arange(len(sX))
                valXaxes = np.arange(len(valX))

                # Do same thing for image plot.
                imData = []
                for key, val in self.alphabet.iteritems():
                    imData.append((key, val))
                x, y = zip(*imData)
                xAx = np.arange(len(x))

                # Create first plot. This plot is a histogram for scrambledData (Symbol-pairs).
                fig1 = plt.figure(1)
                plt.title('Pairs of symbols (No order)')
                ax = fig1.gca()
                ax.bar(sXaxes + 0.6, sY)
                ax.set_xticks(sXaxes + 1)
                ax.set_xticklabels(sX)
                ax.set_xlabel('Symbol-pairs')
                ax.set_ylabel('Number of occurrences (Normalized)')
                ax.set_xlim(0.0, sXaxes.max() + 2)
                if save == 1:
                    # Save plots
                    plt.savefig('model2Plot1.png')

                 # Create second plot. This plot is a histogram for sortedVals (Symbol-pairs).
                fig2 = plt.figure(2)
                plt.title('Symbol-pairs arranged by ascending values. (Doubles only represented once)')
                ax = fig2.gca()
                ax.bar(valXaxes + 0.6, valY)
                ax.set_xticks(valXaxes + 1)
                ax.set_xticklabels(valX)
                ax.set_xlabel('Symbol-pairs')
                ax.set_ylabel('Number of occurrences (Normalized)')
                ax.set_xlim(0.0, valXaxes.max() + 2)
                if save == 1:
                    # Save plots
                    plt.savefig('model2Plot2.png')

                # Create third plot. This plot is an image showing the transfer-probabilities.
                fig3 = plt.figure(3)
                plt.imshow(self.pairTableArray)
                plt.title('Pairs of symbols (No order)')
                ax = fig3.gca()
                ax.set_xticks(xAx)
                ax.set_xticklabels(x)
                ax.set_yticks(xAx)
                ax.set_yticklabels(x)
                ax.set_xlabel('Symbol-pairs')
                ax.set_ylabel('Symbol-pairs')
                plt.colorbar()
                if save == 1:
                    # Save plots
                    plt.savefig('model2Plot3.png')

                if show == 1:
                    # Show plots
                    plt.show()
                elif show == 0:
                    pass
                else:
                    print "Argument show must be 0 or 1."
                if save == 0:
                    pass
                elif save != 1:
                    print "Argument save must be 0 or 1."
            else:
                print "The model selected has not yet been initialized for this object."
        elif model == 3:
            if len(self.normWordPairs) > 0:
                # For Words
                sortedVals = []
                takenVals = []
                # Append from normWordPairs, all values to sortedVals.
                for key, val in self.normWords.iteritems():
                    if val not in takenVals:
                        sortedVals.append(val)
                        takenVals.append(val)
                # Sort the list, then find the corresponding keys in normWordPairs,
                # and replace list elements with both key and val.
                sortedVals.sort()
                for j, i in enumerate(sortedVals):
                    for key in self.normWords:
                        if self.normWords[key] == i:
                            sortedVals[j] = (key, i)
                # Create list with (key, val) elements for scrambled data plot.
                scrambledData = []
                for key, val in self.normWords.iteritems():
                    scrambledData.append((key, val))
                # Zip the sorted list and the scrambled list.
                sX, sY = zip(*scrambledData)
                valX, valY = zip(*sortedVals)
                # Define x-axes
                sXaxes = np.arange(len(sX))
                valXaxes = np.arange(len(valX))

                # For wordPairs
                sortedpairVals = []
                takenpairVals = []
                # Append from normWordPairs, all values to sortedpairVals.
                for key, val in self.normWordPairs.iteritems():
                    if val not in takenpairVals:
                        sortedpairVals.append(val)
                        takenpairVals.append(val)
                # Sort the list, then find the corresponding keys in normWordPairs,
                # and replace list elements with both key and val.
                sortedpairVals.sort()
                for j, i in enumerate(sortedpairVals):
                    for key in self.normWordPairs:
                        if self.normWordPairs[key] == i:
                            sortedpairVals[j] = (key, i)
                # Create list with (key, val) elements for scrambled data plot.
                scrambledpairData = []
                for key, val in self.normWordPairs.iteritems():
                    scrambledpairData.append((key, val))
                # Zip the sorted list and the scrambled list.
                spairX, spairY = zip(*scrambledpairData)
                valpairX, valpairY = zip(*sortedpairVals)
                # Define x-axes
                spairXaxes = np.arange(len(spairX))
                valpairXaxes = np.arange(len(valpairX))

                # Do same thing for image plot.
                imData = []
                for key, val in self.words.iteritems():
                    imData.append((key, val))
                x, y = zip(*imData)
                xAx = np.arange(len(x))

                # Create first plot. This plot is a histogram for scrambledData (Words).
                fig1 = plt.figure(1)
                plt.title('Words (No order)')
                ax = fig1.gca()
                ax.bar(sXaxes + 0.6, sY)
                ax.set_xticks(sXaxes + 1)
                ax.set_xticklabels(sX)
                ax.set_xlabel('Words')
                ax.set_ylabel('Number of occurrences (Normalized)')
                ax.set_xlim(0.0, sXaxes.max() + 2)
                if save == 1:
                    # Save plots
                    plt.savefig('model3Plot1.png')

                 # Create second plot. This plot is a histogram for sortedVals (Words).
                fig2 = plt.figure(2)
                plt.title('Words arranged by ascending values. (Doubles only represented once)')
                ax = fig2.gca()
                ax.bar(valXaxes + 0.6, valY)
                ax.set_xticks(valXaxes + 1)
                ax.set_xticklabels(valX)
                ax.set_xlabel('Words')
                ax.set_ylabel('Number of occurrences (Normalized)')
                ax.set_xlim(0.0, valXaxes.max() + 2)
                if save == 1:
                    # Save plots
                    plt.savefig('model3Plot2.png')

                # For word-pairs
                # Create third plot. This plot is a histogram for scrambledData (Word-pairs).
                fig1 = plt.figure(3)
                plt.title('Pairs of words (No order)')
                ax = fig1.gca()
                ax.bar(spairXaxes + 0.6, spairY)
                ax.set_xticks(spairXaxes + 1)
                ax.set_xticklabels(spairX)
                ax.set_xlabel('Word-pairs')
                ax.set_ylabel('Number of occurrences (Normalized)')
                ax.set_xlim(0.0, spairXaxes.max() + 2)
                if save == 1:
                    # Save plots
                    plt.savefig('model3Plot3.png')

                # Create fourth plot. This plot is a histogram for sortedVals (Word-pairs).
                fig2 = plt.figure(4)
                plt.title('Word-pairs arranged by ascending values. (Doubles only represented once)')
                ax = fig2.gca()
                ax.bar(valpairXaxes + 0.6, valpairY)
                ax.set_xticks(valpairXaxes + 1)
                ax.set_xticklabels(valpairX)
                ax.set_xlabel('Word-pairs')
                ax.set_ylabel('Number of occurrences (Normalized)')
                ax.set_xlim(0.0, valpairXaxes.max() + 2)
                if save == 1:
                    # Save plots
                    plt.savefig('model3Plot4.png')

                # Create fifth plot. This plot is an image showing the transfer-probabilities.
                fig3 = plt.figure(5)
                plt.imshow(self.wordPairTableArray)
                plt.title('Pairs of words (No order)')
                ax = fig3.gca()
                ax.set_xticks(xAx)
                ax.set_xticklabels(x)
                ax.set_yticks(xAx)
                ax.set_yticklabels(x)
                ax.set_xlabel('word-pairs')
                ax.set_ylabel('word-pairs')
                plt.colorbar()
                if save == 1:
                    # Save plots
                    plt.savefig('model3Plot3.png')

                if show == 1:
                    # Show plots
                    plt.show()
                elif show == 0:
                    pass
                else:
                    print "Argument show must be 0 or 1."
                if save == 0:
                    pass
                elif save != 1:
                    print "Argument save must be 0 or 1."
            else:
                print "The model selected has not yet been initialized for this object."
        else:
            print "Model argument must be ints 1, 2 or 3, representing text generator model."
