import nltk
import os.path

phrase_start_length = 5
phrases = [] # list of lists of phrases - each sublist stores each length of phrase

def phrase_in_list_ignorecase(new_phrase, phrase_list): # return which phrase_num is match
    if phrase_list == []:
        return -1
    new_phrase_low = new_phrase.lower()
    for phrase_num, phrase in enumerate(phrase_list):
        phrase_low = phrase[0].lower()
        if phrase_low == new_phrase_low:
            return phrase_num
    return -1

def sorted_list_by_length(length):
    return sorted(phrases[length-phrase_start_length], key=lambda x: len(x[1]), reverse=True)

def read_text(textName, ignoreChars = []):
    file = open(textName, "r")
    text = file.read()
    file.close()
    paragraphs = text.split("\n\n")
    phrase_length = phrase_start_length
    while True:  # Keep going until we reach a phrase length where no repetition occurs
        phrases.append([])
        paragraph_count = 0
        sentence_count = 0
        word_count = 0
        for paragraph_num, paragraph in enumerate(paragraphs):
            if paragraph_count % 100 == 0:
                print(paragraph_count)
            paragraph_count += 1
            #p_tokens = nltk.sent_tokenize(paragraph)
            #full_sentence = ""
            #for sentence_num, sentence in enumerate(p_tokens):
            #    sentence_count += 1
            #    full_sentence += sentence + "\n"
        
            #s_tokens = nltk.word_tokenize(full_sentence)
            s_tokens = nltk.word_tokenize(paragraph)
            
            # optional field to ignore certain chars, as tokenization counts them as tokens
            if len(ignoreChars) > 0:
                s_tokens = [x for x in s_tokens if not x in ignoreChars]
            
            word_count += len(s_tokens)
            for word_num, word in enumerate(s_tokens):
                new_phrase = ""
                if len(s_tokens) - word_num >= phrase_length: # enough in current line
                    for phrase_index in range(phrase_length):
                        new_phrase += s_tokens[word_num+phrase_index] + " "
                
                    phrase_num = phrase_in_list_ignorecase(new_phrase, phrases[phrase_length - phrase_start_length])
                    if phrase_num == -1:
                        phrases[phrase_length - phrase_start_length].append([new_phrase, [paragraph_num]])
                    else:
                        phrases[phrase_length - phrase_start_length][phrase_num][1].append(paragraph_num)

        # remove phrases with only one occurrence
        removals = []
        for phrase in phrases[phrase_length - phrase_start_length]:
            if len(phrase[1]) == 1:
                removals.append(phrase)
        for removal in removals:
            phrases[phrase_length - phrase_start_length].remove(removal)

        # if the most commonly occurring phrase at this length only occurs once, pop and exit
        sorted_list = sorted_list_by_length(phrase_length)
        if len(sorted_list) < 1  or len(sorted_list[0][1]) <= 1:
            phrases.pop()
            break
        
        # repetition still being found, continue to next phrase length
        print(phrase_length)
        phrase_length += 1

def remove_subsumed():
    for phrase_set_num, phrase_set in enumerate(phrases): # for each length of phrase
        phrases_to_remove = []
        for phrase in phrase_set: # for each phrase in that set
            for phrase_set_num_2, phrase_set_2 in enumerate(phrases): # compare each phrase to other phrase sets
                if phrase_set_num >= phrase_set_num_2: # don't compare with same length or smaller
                    continue
                for phrase_2 in phrase_set_2: # compare each phrase to each phrase in other phrase sets
                    if phrase[0] in phrase_2[0]: # is smaller phrase subsumed by larger
                        removals = [] # can't remove from list while iterating over it
                        for phrase_occurance in phrase[1]:
                            if phrase_occurance in phrase_2[1]:
                                removals.append(phrase_occurance)
                        for removal in removals:
                            phrase[1].remove(removal)
                        if len(phrase[1]) == 0: # all occurances have been subsumed - remove
                            phrases_to_remove.append(phrase)

        for phrase_removal in phrases_to_remove:
            if phrase_removal in phrase_set:
                phrase_set.remove(phrase_removal)

        # after removing sub-phrases which are completely subsumed, some phrases may only be
        # listed as occurring once

def print_all():
    for phrase_length, phrase in enumerate(phrases):
        print (sorted_list_by_length(phrase_length+phrase_start_length))
        print("")

# writes all phrase data to the desired file name. If the file exists, a new file is
# created with a greater index so older data is preserved
def write_all_to_file(textType):
    filePath = "Phrase_Data_" + textType
    if os.path.exists(filePath + ".txt"):
        file_index = 0
        while os.path.exists(filePath + "_" + str(file_index) + ".txt"):
            file_index += 1
        filePath = filePath + "_" + str(file_index) + ".txt"
    else:
        filePath += ".txt"
    file = open(filePath, "w")
    
    for phrase_length, phrase in enumerate(phrases):
        file.write(str(phrase_length + phrase_start_length) + " : " + str(sorted_list_by_length(phrase_length+phrase_start_length)) + "\n\n")

    file.close()


# parse the saved phrases and store in useable variable
def read_saved_phrases(url):
    if os.path.exists(url):
        file = open(url, "r")
        text = file.read()
        file.close()
        
        set_min_length = True
        phrases = []
        paragraphs = text.split("\n\n")
        
        for paragraph in paragraphs:
            split_paragraph = paragraph.split(" : ")
            if(len(split_paragraph) < 2):
                continue
        
            phrase_list = []
            
            if set_min_length:
                phrase_start_length = int (paragraph.split(" : ")[0])
                set_min_length = False
            
            only_phrases = paragraph.split(" : ")[1]
            only_phrases = only_phrases[2:-2] # remove [[ and ]]
            only_phrases = only_phrases.split("], [")
            for phrase in only_phrases:
                phrase = phrase[1:-1]
                split_phrase = phrase.split("\', [")
                new_phrase = split_phrase[0]
                phrase_occurances = split_phrase[1].split(", ")
                phrase_occurances_list = []
                for phrase_occurance in phrase_occurances:
                    phrase_occurances_list.append(int(phrase_occurance))
                
                phrase_list.append([new_phrase, phrase_occurances_list])

            phrases.append(phrase_list)
        print(phrases)
            #for char_index, char in enumerate(paragraph):

    else:
        print("File not found")


readFile = "Full"
#readFile = "Single"
#readFile = "Test"

#read_text(readFile + ".txt", ['.', ','])

#remove_subsumed()

#print_all()

#write_all_to_file(readFile)

read_saved_phrases("Phrase_Data_Single_0.txt")





