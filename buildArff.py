import os
import string
from collections import OrderedDict

#####################################################################################
##     Method buildArff() reads a file with tagged tweets and outputs an arff file
##     for use with Weka. Input and output filenames are currently hard-coded;
##     this can be modified to pass the filenames as parameters (program must be run
##     the command line to pass paramters). It is assumed that the input file is in the
##     same directory as the buildArff() method.
##
##     Input format:
##
##           <digit> , <tagged_words>
##
##     where <digit> is either 0 or 4, indicating the sentiment of the tweet as given
##     in the training data; a comma follows <digit>, and <tagged_words> is a series
##     of <word_PoS> comprising the tagged tokens in the tweet, where "word" and "PoS"
##     are connected with the character "_", and sequential <word_PoS> items are separated
##     with blanks. Each tweet ends with a carriage return.
##
##     Output is written to a file in the same directory as the buildArff() method;
##     again the filename is currently hard-coded.
#####################################################################################


def is_punct_string(s):
    # check if string consists only of punctuation 
    for char in s:
       if not char in string.punctuation:
           return False
    return True

def is_digit_string(s):
    # check if string consists only of digits 
    for char in s:
       if not char.isdigit():
           return False
    return True

def is_all_upper(s):
    # check if string contins all upper case characters
    for char in s:
       if not char.isupper():
           return False
    return True

# A filter to aid in feature selection, currently unused.
# Modify this to do more sophisticated feature selection.
def featurePassesFilter(feature):

    if feature.isdigit():
        return False
    return True

# Build a dicitonary whose keys are possible values for tokens and tags,
# each of which is associated with the feature it represents.
# This is where you can add specific tokens and tags that increment
# their associated feature counts.
def buildFeatureDictionary():
    dictionary = {
        "A":"Pu",
        "G":"Pu",
        "C":"Py",
        "U":"Py",
        "G":"Three-H-Sites",
        "C":"Three-H-Sites",
        "A":"Two-H-Sites",
        "T":"Two-H-Sites",
        
        }
    
    return OrderedDict(sorted(dictionary.items(), key = lambda t:t[0]))

# Build a list of features that will be included in the arff file.
# This is where to add feature names if desired. Additional feature
# names shoud be added BEFORE "Average_token_length" and "Sentiment",
# which must be the last two features in the list
def buildFeatureList():

    feature_list = [
        "Pu",
        "Py",
        "Three-H-Sites",
        "Two-H-Sites"]
    return feature_list

# Write the arff header to the output file 
def writeArffHeader(outfile,relation_name,feature_list):

    # Write out the first line with the Relation name
    outfile.write("@RELATION " + relation_name + "\n\n")

    # Write out the feature names and their types
    for feature_name in feature_list:
        
        outfile.write("@ATTRIBUTE\t\"" + feature_name + "\"\tNUMERIC\n")

    # Write out the data header
    outfile.write("\n@DATA\n\n")
    
# Writes the feature vector for a tweet to the @DATA section of the arff file
def writeInstance(outfile,feature_list,feature_vector):

    for feature in feature_list[:-2]:
        outfile.write(str(feature_vector[feature]) + ",")

# Creates and initializes a new feature vector for a tweet
def createFeatureVector(feature_list):
    feature_vector = {}
    
    for feature in feature_list:
        feature_vector[feature] = 0
    return feature_vector

# Iterates through the token/tag pairs in a tweet and increments feature
# counts. 
def buildFeatureVector(tweet,feature_list,feature_dict):
    # Get a new initialized feature vector for this tweet
    feature_vector = createFeatureVector(feature_list)

    return feature_vector

# To execute this file, run the file and then enter the command buildArff() on the Python shell command line
def buildArff():
    # Retrieve the path of the current directory (the one continaing this code)
    curdir = os.getcwd()
    # Create the path name to the input file, assumed to be in the current directory.
    # Change this to get the filename from input parameters 
    infile_name = os.path.join(curdir,"test_file.txt")
    # Output written to a file in the current directory (by default).
    # Change this to get the filename from input parameters 
    outfile_name = "seq.arff"

    # Create the dictionary of "string", "feature type" pairs, and the list of features
    feature_dict= buildFeatureDictionary()
    feature_list = buildFeatureList()

    # Open the output file and write the arff header
    outfile = open(outfile_name,"w")

    writeArffHeader(outfile,"seq-res",feature_list)

    # Read each line of the input file (assumed each is one tweet) and build
    # a vector of feature counts for the tweet, then append to the arff file
    infile = open(infile_name)
    for tweet in infile:
        feature_vector = buildFeatureVector(tweet,feature_list,feature_dict)
        writeInstance(outfile,feature_list,feature_vector)
   

        