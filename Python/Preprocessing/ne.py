import nltk
from nltk.corpus import conll2002, ieer
from nltk.sem import extract_rels,rtuple
import nltk.tag, nltk.data
from fyp import print_chunks, adjust_ne
import re

class doc:
    headline = None
    text = None

vnv = """
is|    # 3rd sing present and
was/V|   # past forms of the verb zijn ('be')
werd/V|  # and also present
wordt/V  # past of worden ('become)
.*       # followed by anything
"""
VAN = re.compile(vnv, re.VERBOSE)

additional_nes = ["I", "Troy"]

'''
    
    As it stands, I can get regular expressions to work to both identify which 
    words should be included in chunks, as well as specify what words to search
    for between named entities. This type of search works for hard-coded input 
    but doesn't seem to be working for the chunked objects. This may either be
    because of the format of the trees produced by chunking differing from that
    of the hard-coded example, or because of the POS tags generated not matching
    the search parameters. I think I will need to customise the tags, limiting
    them to a particular desired tag or something.
    
    http://www.nltk.org/book/ch07.html
    http://stackoverflow.com/questions/7851937/extract-relationships-using-nltk
    http://www.regular-expressions.info/wordboundaries.html
    http://delivery.acm.org/10.1145/1130000/1123138/p39-chau.pdf?ip=137.43.22.72&id=1123138&acc=ACTIVE%20SERVICE&key=846C3111CE4A4710%2EFFC467975145E027%2E4D4702B0C3E38B35%2E4D4702B0C3E38B35&CFID=860543845&CFTOKEN=79758959&__acm__=1478093370_70b65819aa187b319cd2cd5deb7da3a2
    http://stackoverflow.com/questions/7851937/extract-relationships-using-nltk/7853030#7853030
    
    adding /IN to the end of the regex search elements didn't work. I had hoped 
    that what was going wrong was that I was searching for "in" when the 
    representation in the tree is in fact "in/IN" with its POS tag. Doesn't seem
    to be the case. Definitely gonna have to try to print out individual
    components of the chunked tree to see how it really looks in comparison to 
    the hard coded tree.
'''

'''
        Must hard code list of exceptions to POS tagging, as many words are being picked up erroniously
'''




pattern = """
NP: {<NNP>+}
""" # define a tag pattern of an NP chunk
NPChunker = nltk.RegexpParser(pattern) # create a chunk parser
preposition = re.compile (r'.*\bin\b(?!\b.+ing)|.*\bat\b|.*\baround\b')

default_tagger = nltk.data.load(nltk.tag._POS_TAGGER)
model = {'I': 'NP'}
tagger = nltk.tag.UnigramTagger(model=model, backoff=default_tagger)

file = open("Full Text.txt", "r")
#file = open("Single.txt", "r")
text = file.read()
file.close()
paragraph_count = 0
sentence_count = 0
word_count = 0
ne_count = 0
ne_set = []
paragraphs = text.split("\n\n")
for paragraph in paragraphs:
    paragraph_count += 1
    p_tokens = nltk.sent_tokenize(paragraph)
    for sentence in  p_tokens:
        sentence_count += 1
        s_tokens = nltk.word_tokenize(sentence)
        word_count += len(s_tokens)
        #tagged = nltk.pos_tag(s_tokens)
        tagged = tagger.tag(s_tokens)
        chunks = nltk.ne_chunk(tagged, binary=True)
        
        for chunk in chunks:
            if type(chunk).__name__=="Tree":
                ne_count += 1
                if not chunk in ne_set:
                    ne_set.append(chunk)
        
        #chunks = adjust_ne(chunks, additional_nes) #Adjust chunks, adding NEs where needed
        '''
        #chunks = NPChunker.parse(tagged)
        #print_chunks(chunks)
        doc.headline = ['foo']
        #print (type(chunks).__name__)
        ''''''doc.text = [     nltk.Tree('ORGANIZATION', ['Somebody']),     'is', 'living', 'around', 'the',    nltk.Tree('LOCATION',['Philadelphia']),      nltk.Tree('PERSON', ['Gross'])     ]''''''
        doc.text = [chunks]
        print(chunks)
        #print_chunks(chunks)
        
        for r in nltk.sem.extract_rels('PER', 'ORG', sentence, corpus='ace', pattern=preposition):
            #print("a")
            #print (nltk.sem.relextract.rtuple(r))
            print('{0:<5}{1}'.format(i, rtuple(r)))
            #print(chunks)
            #print (chunks)'''
"""tokens = nltk.word_tokenize(text)
tagged = nltk.pos_tag(tokens)
chunk = nltk.ne_chunk(tagged, binary=True)
print_chunks(chunk)"""

print ("Paragraph Count : " + str(paragraph_count))
print ("Sentece Count : " + str(sentence_count))
print ("Word Count : " + str(word_count))
print ("Ne Count : " + str(ne_count))
print ("Distinct Ne Count : " + str(len(ne_set)))
