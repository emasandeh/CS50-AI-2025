import nltk
import sys
import re

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP Pred | S ConjP
Pred ->  Adv Pred | VP | Pred Adv
ConjP -> Conj VP | Conj S 
AP -> Adj N | Adj AP
NP -> N | AP | Det AP | Det N
PP -> P NP | PP PP
VP -> V | V NP | V Adv | V PP | V NP PP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    tockenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    sentenceL = tockenizer.tokenize(sentence.lower())
    return list(filter(lambda x: not re.findall('[a-zA-Z]', x) == [], sentenceL))


def np_chunk(tree):
    np_chunks = []
    for subtree in tree.subtrees():
        if subtree.label() == "NP":
            np_chunks.append(subtree)

    return np_chunks


if __name__ == "__main__":
    main()
 # type: ignore