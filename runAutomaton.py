from AutomaticTextGenerator import AutomaticTextGenerator
import time

if __debug__:
    print "~"*80
    print "In debug mode."
    print "~"*80
else:
    print "~"*80
    print "In non-debug mode."
    print "~"*80

print "Welcome to the test file for AutomaticTextGenerator."
print "Average run-time for this file: 1.5 minutes. (With no inputs or plots, and excluding the final tests.)"
print "All tests are optional."

Q1 = raw_input("Do you want to run positive tests? ('n' for no, any other key for yes.)")

if Q1 != 'n':
    print "~"*80
    print "Following code will run most important tests of the AutomaticTextGenerator class, " \
          "and gather some run-time statistics."
    print "First it will initialize a new object for each mode."
    raw_input("Press Enter to continue...")

    print "~"*80
    print "Initializing new AutomaticTextGenerator object, as model 1."
    iniStart = time.clock()
    start = time.clock()
    newTextGenerator1 = AutomaticTextGenerator(1)
    newTextGenerator1.defineAlphabet("ABCs.txt")
    newTextGenerator1.feedInput("ugeseddel_data.txt")
    newTextGenerator1.identifyProbabilities()
    stop = time.clock()
    oneT = stop - start
    print "~"*80
    print "Initializing new AutomaticTextGenerator object, as model 2."
    start = time.clock()
    newTextGenerator2 = AutomaticTextGenerator(2)
    newTextGenerator2.defineAlphabet("ABCs.txt")
    newTextGenerator2.feedInput("ugeseddel_data.txt")
    newTextGenerator2.identifyProbabilities()
    stop = time.clock()
    twoT = stop - start
    print "~"*80
    print "Initializing new AutomaticTextGenerator object, as model 3."
    start = time.clock()
    newTextGenerator3 = AutomaticTextGenerator(3)
    newTextGenerator3.defineAlphabet("ABCs.txt")
    newTextGenerator3.feedInput("ugeseddel_data.txt")
    newTextGenerator3.identifyProbabilities()
    stop = time.clock()
    threeT = stop - start
    iniStop = time.clock()
    iniT = iniStop - iniStart
    print "~"*80
    print "Initializing each of the models took: " \
          "\n Model 1 {0} seconds. \n Model 2 {1} seconds. \n Model 3 {2} seconds.".format(oneT, twoT, threeT)
    print
    print "Next a new object will be initialized for all three models. The other objects will be dumped."
    raw_input("Press Enter to continue..")
    print "Deleting old objects."
    del newTextGenerator1, newTextGenerator2, newTextGenerator3
    start = time.clock()
    print "~"*80
    print "Initializing object as model 1."
    newTextGenerator = AutomaticTextGenerator(1)
    newTextGenerator.defineAlphabet("ABCs.txt")
    newTextGenerator.feedInput("ugeseddel_data.txt")
    newTextGenerator.identifyProbabilities()
    print "~"*80
    print "Changing to model 2."
    newTextGenerator.changeModel(2)
    print "~"*80
    print "Changing to model 3."
    newTextGenerator.changeModel(3)
    stop = time.clock()
    allIn = stop-start
    print "~"*80
    print "The object is now ready to generate texts for each model."
    print "Initializing object for all 3 models took {0} seconds.".format(allIn)
    print "It will now generate 10 texts containing 1000 symbols for each model. (Prints, but does not save)"
    print "It will start by generating model 1 texts, then model 2, then model 3."
    raw_input("Press Enter to continue...")
    print "~"*80
    print "Change to model 1 and generate texts."
    genStart = time.clock()
    start = time.clock()
    newTextGenerator.changeModel(1)
    for i in range(10):
        newTextGenerator.generateText(1000)
        print "~"*80
        print "Model 1 text", i+1
        print newTextGenerator.newtext
    stop = time.clock()
    gen1T = stop - start
    print "~"*80
    print "Change to model 2 and generate texts."
    start = time.clock()
    newTextGenerator.changeModel(2)
    for i in range(10):
        newTextGenerator.generateText(1000)
        print "~"*80
        print "Model 2 text", i+1
        print newTextGenerator.newtext
    stop = time.clock()
    gen2T = stop - start
    print "~"*80
    print "Change to model 3 and generate texts."
    start = time.clock()
    newTextGenerator.changeModel(3)
    for i in range(10):
        newTextGenerator.generateText(1000)
        print "~"*80
        print "Model 3 text", i+1
        print newTextGenerator.newtext
    stop = time.clock()
    gen3T = stop - start
    genStop = time.clock()
    genTotal = genStop - genStart
    print "~"*80
    print "(After first initializing)"
    print "Changing models and generating 10 new texts took for each model:" \
          "\n Model 1: {0} seconds. \n Model 2: {1} seconds. \n Model 3: {2} seconds.".format(gen1T, gen2T, gen3T)
    print "Total time to do this: {0} seconds.".format(genTotal)
    print
    print "To demonstrate that saving a new text does indeed work, the program will now save one of each texts."
    raw_input("Press Enter to continue...")
    newTextGenerator.changeModel(1)
    newTextGenerator.generateText(1000)
    newTextGenerator.saveText("newText")
    newTextGenerator.changeModel(2)
    newTextGenerator.generateText(1000)
    newTextGenerator.saveText("newText")
    newTextGenerator.changeModel(3)
    newTextGenerator.generateText(1000)
    newTextGenerator.saveText("newText")
    print "~"*80
    print "You should now be able to locate the files in the directory."
    print
    print "Statistics for run-time:"
    print "Initialising new objects with the models:" \
          " \n Model 1: {0} seconds. \n Model 2: {1} seconds. \n Model 3: {2} seconds. \n Total time: {3} seconds." \
          "".format(oneT, twoT, threeT, iniT)
    print "Initialising one object to each model: \n Total time: {0} seconds.".format(allIn)
    print "Generating 10 texts (and changing between initialised models):" \
          " \n Model 1: {0} seconds. \n Model 2: {1} seconds. \n Model 3: {2} seconds.".format(gen1T, gen2T, gen3T)
    print "Total time to generate these 30 new texts: \n {0} seconds".format(genTotal)
    print
    raw_input("Press Enter to continue...")

print "~"*80
Q2 = raw_input("Do you want to run negative tests? ('n' for no, any other key for yes.)")

if Q2 != 'n':
    print "~"*80
    print "First initialise new object for all models."
    negativeGenerator = AutomaticTextGenerator(1)
    negativeGenerator.defineAlphabet("ABCs.txt")
    negativeGenerator.feedInput("ugeseddel_data.txt")
    negativeGenerator.identifyProbabilities()
    print "~"*80
    print "Try generating text with negative N (-10)"
    try:
        negativeGenerator.generateText(-10)
    except:
        print "Raises error, because N must be a positive integer above 0."
    raw_input("Press Enter to continue...")
    print "~"*80
    print "Try defining new alphabet with wrong encoding. (on same object)"
    try:
        negativeGenerator.defineAlphabet("falseABCs.txt")
    except:
        print "Raises error because file is not UTF-8 encoded."
    raw_input("Press Enter to continue...")
    print "~"*80
    print "Try feeding new file with wrong encoding. (on same object)"
    try:
        negativeGenerator.feedInput("falseData.txt")
    except:
        print "Raises error because file is not UTF-8 encoded."
    raw_input("Press Enter to continue...")
    print "~"*80
    print "Initialise new object, but don't call initialisation methods."
    newNegativeGenerator = AutomaticTextGenerator(1)
    print "Then try to initialise methods in wrong order."
    try:
        newNegativeGenerator.feedInput("ugeseddel_data.txt")
    except:
        print "1. Feeding input first, raises error because alphabet has not been defined."
    try:
        newNegativeGenerator.identifyProbabilities()
    except:
        print "2. Identifying probabilities first, raises error because alphabet and input has not been defined."
    try:
        newNegativeGenerator.generateText(1000)
    except:
        print "3. Generating text first, raises error because there is no data to use."
    try:
        newNegativeGenerator.visualizeData(1, 1, 1)
    except:
        print "4. Visualising data first, raises error because there is no data to use."
    print
    raw_input("Press Enter to continue...")

print "~"*80
Q3 = raw_input("Do you want to run plot-tests? ('n' for no, any other key for yes.)")

if Q3 != 'n':
    Q31 = raw_input("Do you want to show plots? ('n' for no, any other key for yes.)")
    Q32 = raw_input("Do you want to save plots? ('n' for no, any other key for yes.)")
    print "~"*80
    print "First initialises new object, for each model."
    raw_input("Press Enter to continue...")
    plottingGenerator = AutomaticTextGenerator(1)
    plottingGenerator.defineAlphabet("ABCs.txt")
    plottingGenerator.feedInput("ugeseddel_data.txt")
    plottingGenerator.identifyProbabilities()
    plottingGenerator.changeModel(2)
    plottingGenerator.changeModel(3)
    print "~"*80
    print "Now generates plots for each model."
    raw_input("Press Enter to continue...")
    try:
        if Q31 != 'n' and Q32 != 'n':
            print "Showing plots for model 1:"
            print "Close plot windows to continue..."
            plottingGenerator.visualizeData(1, 1, 1)
            print "Showing plots for model 2 (Might take a while):"
            print "Close plot windows to continue..."
            plottingGenerator.visualizeData(2, 1, 1)
            print "Showing plots for model 3 (Might take a while):"
            print "Close plot windows to continue..."
            plottingGenerator.visualizeData(3, 1, 1)
        elif Q31 != 'n' and Q32 == 'n':
            print "Showing plots for model 1:"
            print "Close plot windows to continue..."
            plottingGenerator.visualizeData(1, 1, 0)
            print "Showing plots for model 2 (Might take a while):"
            print "Close plot windows to continue..."
            plottingGenerator.visualizeData(2, 1, 0)
            print "Showing plots for model 3 (Might take a while):"
            print "Close plot windows to continue..."
            plottingGenerator.visualizeData(3, 1, 0)
        elif Q31 == 'n' and Q32 != 'n':
            print "Generating and saving plots."
            plottingGenerator.visualizeData(1, 0, 1)
            plottingGenerator.visualizeData(2, 0, 1)
            plottingGenerator.visualizeData(3, 0, 1)
        elif Q31 == 'n' and Q32 == 'n':
            print "Generating plots. Not showing or saving."
            plottingGenerator.visualizeData(1, 0, 0)
            plottingGenerator.visualizeData(2, 0, 0)
            plottingGenerator.visualizeData(3, 0, 0)
    except:
        print "Something went wrong. Please try running code again."
    print
    raw_input("Press Enter to continue...")

print "~"*80
Q4 = raw_input("Do you want to run 'other texts' test?('n' for no, any other key for yes.)")

if Q4 != 'n':
    print "Inititalises new text generator object."
    extraGenerator = AutomaticTextGenerator(3)
    extraGenerator.defineAlphabet("ABCs.txt")
    print "~"*80
    Q41 = raw_input("Do you want to run 'Introduction to Programming' test?(662KB)('n' for no, any other key for yes.)")
    if Q41 != 'n':
        print "Please wait. This may take some time. (approx. 5 minutes)"
        startBook = time.clock()
        extraGenerator.feedInput("PoMBook.txt")
        extraGenerator.identifyProbabilities()
        extraGenerator.generateText(1000)
        extraGenerator.saveText('PoM_newtext')
        stopBook = time.clock()
        bookT = stopBook - startBook
        print "~"*80
        print "The following text is model 3 used on a 'Introduction to Programming'."
        print extraGenerator.newtext
        print
        print "Now generate and print 5 texts"
        raw_input("Press Enter to continue...")
        fiveBooksStart = time.clock()
        for i in range(5):
            print "~"*80
            extraGenerator.generateText
            print extraGenerator.newtext
        fiveBooksStop = time.clock()
        fiveBooksT = fiveBooksStop - fiveBooksStart
        print
        print "Total number of symbols in the text is: {0}.".format(sum(extraGenerator.alphabet.values()))
        print "Total number of words in the text is: {0}.".format(sum(extraGenerator.words.values()))
        print "It took {0} seconds to intitalize and generate a new text.".format(bookT)
        print "Generating 5 new texts took {0} seconds.".format(fiveBooksT)
        print
        raw_input("Press Enter to continue...")
    Q42 = raw_input("Do you want to run small Bible test?(1097KB)('n' for no, any other key for yes.)")
    if Q42 != 'n':
        print "Please wait. This may take some time. (approx. 15 minutes)"
        startsmallBible = time.clock()
        extraGenerator.feedInput("smallBibletxt.txt")
        extraGenerator.identifyProbabilities()
        extraGenerator.generateText(1000)
        extraGenerator.saveText('smallBible_newtext')
        stopsmallBible = time.clock()
        smallbibleT = stopsmallBible - startsmallBible
        print "~"*80
        print "The following text is model 3 used on a fifth of the bible."
        print extraGenerator.newtext
        print
        print "Now generate and print 5 texts:"
        raw_input("Press Enter to continue...")
        fivesmallBiblesStart = time.clock()
        for i in range(5):
            print "~"*80
            extraGenerator.generateText
            print extraGenerator.newtext
        fivesmallBiblesStop = time.clock()
        fivesmallBiblesT = fivesmallBiblesStop - fivesmallBiblesStart
        print
        print "Total number of symbols in the text is: {0}.".format(sum(extraGenerator.alphabet.values()))
        print "Total number of words in the text is: {0}.".format(sum(extraGenerator.words.values()))
        print "It took {0} seconds to intitalize and generate a new text.".format(smallbibleT)
        print "Generating 5 new texts took {0} seconds.".format(fivesmallBiblesT)
        print
        raw_input("Press Enter to continue...")

print "You have reached the end of the tests."
