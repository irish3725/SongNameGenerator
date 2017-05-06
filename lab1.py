#!/usr/bin/env python
import argparse
import re
from collections import defaultdict
from collections import Counter

# Replace the string value of the following variable with your names.
ME = 'Alex Irish';
COLLABORATORS = ['Stack Overflow','docs.python.org']

"""
"   Takes in infile which is a file containing song information
"   
"   Returns most_common_word() which takes in a word, and returns
"   the most common word to come after that word   
"""
def process_file(infile):
    titles = set()

    # Loop through each line of the file
    for line in infile:
        # remove newline character
        cLine = line.rstrip()
        # add song name to titles
        titles.add(get_song_name(cLine).rstrip())

    # d is my dictionary containing my bigrams 
    d = defaultdict(list)

    # loop over the cleaned titles and compute the bigram counts
    for title in titles:
        words = re.split(' +',title)
        biwords = list()
        if len(words) > 1:
            for x in range(0,len(words)-1):
                d[words[x]].append(words[x+1])
                biwords.append([words[x],words[x+1]])

    # shows my dictionary of bigrams if you want to see that
#    print d

    # using bigram_count, find most common word following 'word'
    """
    "   Takes in a word
    "
    "   Returns the word that most often follows the inputted word
    """
    def most_common_word(word):
        # used Counter().most_common() which is a list with all of
        # words and how often they appear sorted from most common
        # to least common. index [0][0] is first most common word
        return Counter(d[word]).most_common()[0][0]
    
    # return most common word
    return most_common_word

"""
"   Takes in a line from the file
"   
"   Returns the song title from the inputted line in all lowercase and
"   without most punctuation or extra text at end of song title
"""
def get_song_name(line):
    # strip newlines
    cLine = line.rstrip()
    # separate string at last <SEP>
    m = re.search('(.+<SEP>.+<SEP>.+<SEP>)(.+)$', cLine)

    # if regular expression was found
    if m:
        # get the name out of regualar expression
        name = m.group(2)
        # remove everthing after [,(,",or:
        name = re.match('[^(^[^"^:]*',name).group()
        # remove common punctuation
        p = re.compile('(\.|\?|!|&|;)')
        name = p.sub('', name)
        # change all to lowercase
        name = name.lower()
        
        # prints all of the cleaned titles
#        print 'title:', name
        
        # return name
        return name

    return 'pattern not found'

"""
"   Takes in method for finding most common following word (most_common_word()
"   from process_file())
"   Takes in seed_word to start the title
"   Takes in word_number to control how long the title is
"
"   Returns string of new title name. Title is generated based on most common
"   words coming after the previous based on most_common_word()
"""
def name_generator(next_word, seed_word, word_number):
    new_name = seed_word
    cur_word = seed_word
    for x in range(1,word_number):
        cur_word = next_word(cur_word)
        new_name = new_name + " " + cur_word
        
    return new_name

"""
"   Takes in method for finding most common following word (most_common_word()
"   from process_file())
"   
"   Returns nothing, but prints new song title based on user input
"""
def TUI(next_word):
    # ask for seed_word
    seed_word = raw_input('Using the dictionary of song titles, I can create a most popular song title. What would you like to be the first word?\n> ')
    # ask for word_number
    word_number = int(input('How many words long would you like your title?\n> '))
    # print song name using name_generator()
    print 'Your song title is:', name_generator(next_word, seed_word, word_number)



# DON'T WORRY ABOUT CODE BELOW HERE, IT JUST MAKES YOUR LIVE EASIER
def get_file_name():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name')
    return parser.parse_args().file_name

def main():
    print 'CSCI 305 Lab 1 submitted by %s' % ME
    print '  with help from %s\n\n' % ', '.join(COLLABORATORS)
    file_name = get_file_name()
    with open(file_name, 'r') as infile:
        # get method for next word
        next_word = process_file(infile)
        # start text interface to ask user for input
        TUI(next_word)

if __name__ == '__main__':
    main()
