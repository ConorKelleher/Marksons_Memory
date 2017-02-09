import nltk
import os.path

class Phrases(object):
    phrase_start_length = None
    phrases = None # list of lists of phrases - each sublist stores each length of phrase
    textType = None

    def __init__(self, textType, phrase_start_length = 5):
        self.phrases = []
        self.phrase_start_length = phrase_start_length
        self.textType = textType

    def phrase_in_list_ignorecase(self, new_phrase, phrase_list): # return which phrase_num is match
        if phrase_list == []:
            return -1
        new_phrase_low = new_phrase.lower()
        for phrase_num, phrase in enumerate(phrase_list):
            phrase_low = phrase[0].lower()
            if phrase_low == new_phrase_low:
                return phrase_num
        return -1

    def sorted_list_by_length(self, length):
        return sorted(self.phrases[length-self.phrase_start_length], key=lambda x: len(x[1]), reverse=True)

    def read_text(self, ignoreChars = []):
        file = open(self.textType+".txt", "r")
        text = file.read()
        file.close()
        paragraphs = text.split("\n\n")
        phrase_length = self.phrase_start_length
        while True:  # Keep going until we reach a phrase length where no repetition occurs
            self.phrases.append([])
            paragraph_count = 0
            sentence_count = 0
            word_count = 0
            for paragraph_num, paragraph in enumerate(paragraphs):
                if paragraph_count % 100 == 0:
                    print(paragraph_count)
                paragraph_count += 1
        
                s_tokens = nltk.word_tokenize(paragraph)
                
                if len(ignoreChars) > 0:
                    s_tokens = [x for x in s_tokens if not x in ignoreChars]
            
                word_count += len(s_tokens)
                for word_num, word in enumerate(s_tokens):
                    new_phrase = ""
                    if len(s_tokens) - word_num >= phrase_length: # enough in current line
                        for phrase_index in range(phrase_length):
                            new_phrase += s_tokens[word_num+phrase_index] + " "
                
                        phrase_num = self.phrase_in_list_ignorecase(new_phrase, self.phrases[phrase_length - self.phrase_start_length])
                        if phrase_num == -1:
                            self.phrases[phrase_length - self.phrase_start_length].append([new_phrase, [paragraph_num]])
                        else:
                            self.phrases[phrase_length - self.phrase_start_length][phrase_num][1].append(paragraph_num)

            # remove phrases with only one occurrence
            removals = []
            for phrase in self.phrases[phrase_length - self.phrase_start_length]:
                if len(phrase[1]) == 1:
                    removals.append(phrase)
            for removal in removals:
                self.phrases[phrase_length - self.phrase_start_length].remove(removal)

            # if the most commonly occurring phrase at this length only occurs once, pop and exit
            sorted_list = self.sorted_list_by_length(phrase_length)
            if len(sorted_list) < 1  or len(sorted_list[0][1]) <= 1:
                self.phrases.pop()
                break
        
            # repetition still being found, continue to next phrase length
            print(phrase_length)
            phrase_length += 1
        self.remove_subsumed()
        self.write_all_to_file()

    def remove_subsumed(self):
        for phrase_set_num, phrase_set in enumerate(self.phrases): # for each length of phrase
            phrases_to_remove = []
            for phrase in phrase_set: # for each phrase in that set
                for phrase_set_num_2, phrase_set_2 in enumerate(self.phrases): # compare each phrase to other phrase sets
                    if phrase_set_num >= phrase_set_num_2: # don't compare with same length or smaller
                        continue
                    for phrase_2 in phrase_set_2: # compare each phrase to each phrase in other phrase sets
                        if phrase[0] in phrase_2[0]: # is smaller phrase subsumed by larger
                            removals = [] # can't remove from list while iterating over it
                            for phrase_occurrence in phrase[1]:
                                if phrase_occurrence in phrase_2[1]:
                                    removals.append(phrase_occurrence)
                            for removal in removals:
                                phrase[1].remove(removal)
                            if len(phrase[1]) == 0: # all occurrences have been subsumed - remove
                                phrases_to_remove.append(phrase)

            for phrase_removal in phrases_to_remove:
                if phrase_removal in phrase_set:
                    phrase_set.remove(phrase_removal)

            # after removing sub-phrases which are completely subsumed, some phrases may only be
            # listed as occurring once
            
    def print_all(self):
        for phrase_length, phrase in enumerate(self.phrases):
            print (sorted_list_by_length(phrase_length + self.phrase_start_length))
            print("")

    def occurrance_count(self, search):
        count = 0
        for phrase_set in self.phrases:
            for phrase in phrase_set:
                if search in phrase[0]:
                    count += len(phrase[1])
        return count

    def phrases_with_string(self, search):
        output = []
        for phrase_set in self.phrases:
            for phrase in phrase_set:
                if search in phrase[0]:
                    for occurrance in phrase[1]:
                        output.append(phrase[0])
        return output

    def phrases_with_entities(self, entities):
        output = []
        for phrase_set in self.phrases:
            for phrase in phrase_set:
                for entity in entities.get_only_strings():
                    if entity in phrase[0] and not phrase[0] in output:
                        output.append (phrase[0])
        return output

    def entity_occurrence_in_phrases_tuples(self, entities, ignore_empty = False):
        occurrence_tuples = []
        for entity in entities.get_only_strings():
            ne_tuple = [entity, []]
            for phrase_set in self.phrases:
                for phrase in phrase_set:
                    if entity in phrase[0]:
                        ne_tuple[1].extend(phrase[1])
            occurrence_tuples.append(ne_tuple)
        if ignore_empty:
            output = []
            for tuple in occurrence_tuples:
                if len(tuple) > 1:
                    output.append(tuple)
            return output
        else:
            return occurrence_tuples

    def cooccurrences(self, entities, window):
        cooccurrences = []
        
        occurrences = self.entity_occurrence_in_phrases_tuples(entities, True)
        for occurrence_num, occurrence in enumerate(occurrences):
            for other_num, other in enumerate(occurrences):
# shouldn't compare same NE, and if other_num is greater than occurrence_num, we'll be
# doubly counting a relation
# also make sure one NE is not included in the other, as this is trivial and so pointless
                if occurrence_num <= other_num or occurrence[0] == other[0] or occurrence[0] in other[0] or other[0] in occurrence[0]:
                    continue
                for instance in occurrence[1]:
                    for other_instance in other[1]:
                        if abs(instance - other_instance) <= window:
                            cooccurrences.append([occurrence[0], other[0], instance, other_instance])
        return cooccurrences

    # writes all phrase data to the desired file name. If the file exists, a new file is
    # created with a greater index so older data is preserved
    def write_all_to_file(self):
        filePath = "Phrase_Data_" + self.textType
        if os.path.exists(filePath + ".txt"):
            file_index = 0
            while os.path.exists(filePath + "_" + str(file_index) + ".txt"):
                file_index += 1
            filePath = filePath + "_" + str(file_index) + ".txt"
        else:
            filePath += ".txt"
        file = open(filePath, "w")
    
        for phrase_length, phrase in enumerate(self.phrases):
            file.write(str(phrase_length + self.phrase_start_length) + " : " + str(self.sorted_list_by_length(phrase_length + self.phrase_start_length)) + "\n\n")

        file.close()


    # parse the saved phrases and store in useable variable
    def read_saved_phrases(self, index = ""):
        url = "Phrase_Data_" +self.textType+"_"+ str(index) +".txt" if index != "" else "Phrase_Data_"+self.textType+".txt"
        if os.path.exists(url):
            file = open(url, "r")
            text = file.read()
            file.close()
            
            set_min_length = True
            self.phrases = []
            paragraphs = text.split("\n\n")
            
            for paragraph in paragraphs:
                split_paragraph = paragraph.split(" : ")
                if(len(split_paragraph) < 2):
                    continue
        
                phrase_list = []
            
                if set_min_length:
                    self.phrase_start_length = int (paragraph.split(" : ")[0])
                    set_min_length = False
            
                only_phrases = paragraph.split(" : ")[1]
                only_phrases = only_phrases[2:-2] # remove [[ and ]]
                only_phrases = only_phrases.split("], [")
                for phrase in only_phrases:
                    phrase = phrase[1:-1]
                    split_phrase = phrase.split("\', [")
                    if len(split_phrase) < 2: #for some reason, " appearing instead of ' for some
                        split_phrase = phrase.split("\", [")
                    if len(split_phrase) < 2:
                        continue
                    new_phrase = split_phrase[0]
                    phrase_occurrences = split_phrase[1].split(", ")
                    phrase_occurrences_list = []
                    for phrase_occurrence in phrase_occurrences:
                        phrase_occurrences_list.append(int(phrase_occurrence))
                
                    phrase_list.append([new_phrase, phrase_occurrences_list])

                self.phrases.append(phrase_list)
            #print(self.phrases)
                #for char_index, char in enumerate(paragraph):

        else:
            print("File not found")

    def write_to_gephi_file(self, entities, window = 5):
        cooccurrence_quadruples = self.cooccurrences(entities, window)
        cooccurrence_tuples = []
        for quad in cooccurrence_quadruples:
            cooccurrence_tuples.append(quad[:-2])
            #print(quad)

        text = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<gexf xmlns:viz=\"http:///www.gexf.net/1.1draft/viz\" version=\"1.1\" xmlns=\"http://www.gexf.net/1.1draft\">\n<meta lastmodifieddate=\"2017-02-09+00:44\">\n<creator>Gephi 0.7</creator>\n</meta>\n<graph defaultedgetype=\"undirected\" idtype=\"string\" type=\"static\">\n<nodes count=\""
        
        nodes = []
        for tuple in cooccurrence_tuples:
            should_add = True
            for found_tuple in nodes:
                if tuple[0] == found_tuple[0]:
                    should_add = False
                    break
            if should_add:
                nodes.append([tuple[0]])
            should_add = True
            for found_tuple in nodes:
                if tuple[1] == found_tuple[0]:
                    should_add = False
                    break
            if should_add:
                nodes.append([tuple[1]])

        for i in range(len(nodes)):
            nodes[i].append(i)
            #print(nodes[i])


        indexes = []
        for tuple in cooccurrence_tuples:
            new_edge = []
            for node in nodes:
                if tuple[0] == node[0]:
                    new_edge.append(node[1])
            for node in nodes:
                if tuple[1] == node[0]:
                    new_edge.append(node[1])
            indexes.append(new_edge)

        #for index in indexes:
        #    print(index)

        edges = []
        done = []
        for index in indexes:
            if index in done:
                input_index = None
                for search_index, edge in enumerate(edges):
                    if edge[0] == index[0] and edge[1] == index[1] or edge[0] == index[1] and edge[1] == index[1]:
                        input_index = search_index
                        break
                edges[input_index][2] += 1
            else:
                done.append(index)
                edges.append([index[0], index[1], 1])
            
        for i in range(len(nodes)):
            nodes[i][0] = nodes[i][0][:-1]

        for i in range(len(edges)):
            edges[i] = [i, edges[i]]

        text += str(len(nodes)) + "\">\n"

        for node in nodes:
            text += "<node id=\""+str(node[1])+".0\" label=\""+str(node[0])+"\"/>\n"
        text += "</nodes>\n<edges count=\"" + str(len(edges)) + "\">\n"

        for edge in edges:
            text += "<edge id=\""+str(edge[0])+"\" source=\""+str(edge[1][0])+".0\" target=\""+str(edge[1][1])+".0\""
            if edge[1][2] >1:
                text += " weight=\""+str(edge[1][2])+".0\"/>\n"
            else:
                text += "/>\n"

        
        text += "</edges>\n</graph>\n</gexf>\n"
        
        filePath = "Gephi_NE_Relations_" + self.textType + "_Window" + str(window)
        if os.path.exists(filePath + ".gexf"):
            file_index = 0
            while os.path.exists(filePath + "_" + str(file_index) + ".gexf"):
                file_index += 1
            filePath = filePath + "_" + str(file_index) + ".gexf"
        else:
            filePath += ".gexf"
        file = open(filePath, "w")
        file.write(text)
        file.close()

#read_text(readFile + ".txt", ['.', ','])

#remove_subsumed()

#print_all()

#write_all_to_file(readFile)








