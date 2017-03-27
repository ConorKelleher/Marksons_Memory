import nltk
import os.path
import plotly
from random import randint

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


    # old pre-n-grammy code
    def read_text_old(self, ignoreChars = [], unique = False):
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
        self.remove_subsumed(unique)
        self.write_all_to_file(unique)
        
        
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
                
                phrases = nltk.ngrams(s_tokens, phrase_length)
                
                for phrase_num, ngram in enumerate(phrases):
                    phrase = ""
                    for word in ngram:
                        phrase += word + " "
                    phrase_index = self.phrase_in_list_ignorecase(phrase, self.phrases[phrase_length - self.phrase_start_length])
                    if phrase_index == -1:
                        self.phrases[phrase_length - self.phrase_start_length].append([phrase, [paragraph_num]])
                    else:
                        self.phrases[phrase_length - self.phrase_start_length][phrase_index][1].append(paragraph_num)

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
        self.remove_subsumed(False)
        self.write_all_to_file(False)   

    def remove_subsumed(self, unique):
        for phrase_set_num, phrase_set in enumerate(self.phrases): # for each length of phrase
            phrases_to_remove = []
            for phrase in phrase_set: # for each phrase in that set
                for phrase_set_num_2, phrase_set_2 in enumerate(self.phrases): # compare each phrase to other phrase sets
                    if phrase_set_num >= phrase_set_num_2: # don't compare with same length or smaller
                        continue
                    for phrase_2 in phrase_set_2: # compare each phrase to each phrase in other phrase sets
                        if phrase[0] in phrase_2[0]: # is smaller phrase subsumed by larger
                            if unique:
                                phrases_to_remove.append(phrase)
                            else:
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
    def write_all_to_file(self, unique):
        filePath = "Phrase_Data_" + self.textType
        if unique:
            filePath += "_Unique"
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
    def read_saved_phrases(self, index = "", unique = False):
        url = ""
        if index != "":
            if unique:
                url = "Phrase_Data_" +self.textType+"_"+ "Unique_" + str(index) +".txt"
            else:
                url = "Phrase_Data_" +self.textType+"_"+ str(index) +".txt"
        else:
            if unique:
                url = "Phrase_Data_"+self.textType+"Unique.txt"
            else:
                url = "Phrase_Data_"+self.textType+".txt"
            
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
            
    def cooccurrence_clusters(self, entities, window = 5):
        cooccurrence_quadruples = self.cooccurrences(entities, window)
        cooccurrence_tuples = []
        for quad in cooccurrence_quadruples:
            new_tuple = quad[:-2]
            if not new_tuple in cooccurrence_tuples:
                cooccurrence_tuples.append(new_tuple)
            
        clusters = []
        
        tuples_appended = []
        
        for tuple_num, tuple in enumerate(cooccurrence_tuples):
            
            should_add = True
            for tuple2 in tuples_appended:
                if tuple[0] in tuple2 or tuple[1] in tuple2:
                    should_add = False
                    break
            
            if should_add:
                clusters.append(tuple)
                tuples_appended.append(tuple)
            
            while True:
                should_break = True
                
                for tuple2 in cooccurrence_tuples:
                    if tuple == tuple2:
                        continue
                    index_to_add = None
                    cluster_index = len(clusters)-1
                    if tuple2[0] in clusters[cluster_index] and not tuple2[1] in clusters[cluster_index]:
                        clusters[cluster_index].append(tuple2[1])
                        should_break = False
                    elif tuple2[1] in clusters[cluster_index] and not tuple2[0] in clusters[cluster_index]:
                        clusters[cluster_index].append(tuple2[0])
                        should_break = False
                    
                if should_break:
                    break
                    
        return clusters
    
    def num_paragraphs(self):
        file = open(self.textType+".txt", "r")
        text = file.read()
        file.close()
        paragraphs = text.split("\n\n")
        return len(paragraphs)
                
    def cooccurrence_jump_sequences(self, entities, window = 0, min_size = 3):
        all_clusters = self.cooccurrence_clusters(entities, window)
        clusters = [] # to allow keeping only clusters that are big enough
        for cluster in all_clusters:
            if len(cluster) >= min_size:
                clusters.append(cluster)
        
        file = open(self.textType+".txt", "r")
        text = file.read()
        file.close()
        paragraphs = text.split("\n\n")
        
        occurrences = [] # list of lists of paragraph numbers and the cluster jumped to
        
        for paragraph_num, paragraph in enumerate(paragraphs):
            for cluster_num, cluster in enumerate(clusters):
                for ne in cluster:
                    if ne in paragraph:
                        occurrences.append([paragraph_num, cluster_num, ne])
                        
        sequence = []
        last_cluster = -1
        for occurrence in occurrences:
            if occurrence[1] != last_cluster:
                sequence.append(occurrence)
                last_cluster = occurrence[1]
                
        return sequence
            
    def write_to_gephi_file(self, entities, window = 5):
        cooccurrence_quadruples = self.cooccurrences(entities, window)
        cooccurrence_tuples = []
        for quad in cooccurrence_quadruples:
            cooccurrence_tuples.append(quad[:-2])

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

    def write_to_csv(self, min_phrase_length = 0):
        filePath = "Phrase_Occurrences_" + self.textType
        if os.path.exists(filePath + ".csv"):
            file_index = 0
            while os.path.exists(filePath + "_" + str(file_index) + ".csv"):
                file_index += 1
            filePath = filePath + "_" + str(file_index) + ".csv"
        else:
            filePath += ".csv"
        file = open(filePath, "w")

        phrase_length = len(self.phrases) + self.phrase_start_length
        for phrase_set in reversed(self.phrases): # iterate through phrases backwards
            for phrase in phrase_set:
                file.write(str(phrase_length) + "," + str(phrase[0][:-1]))
                for occurrence in phrase[1]:
                    file.write("," + str(occurrence))
                file.write("\n")
            phrase_length -= 1
            if phrase_length < min_phrase_length:
                break
        file.close()

    def network_sequence_graph(self, entities, window, min_network, file_name):
        data = []
        clusters = []
        cluster_colours = [('rgba(50,200,0,1)'), ('rgba(0,200,244,1)'), ('rgba(0,0,247,1)'), ('rgba(220,110,220,1)'), ('rgba(220,0,0,1)')]
        
        cluster_sequence = self.cooccurrence_jump_sequences(entities, window, min_network)
        
        for seq_num, sequence in enumerate(cluster_sequence):
            should_append = True
            for cluster in clusters:
                if sequence[1] == cluster[0]: # network has already been found, only track the ne
                    should_append = False
                    clusters[sequence[1]][1].append(sequence[2])
            if should_append:
                clusters.append([sequence[1], [sequence[2]]])
                
        clusters.sort(key=lambda network: network[0])
                
        for cluster in clusters:
            allWordDist = nltk.FreqDist(cluster[1])
            mostCommon= allWordDist.most_common(1)
            cluster[1] = mostCommon[0][0]
                
        for cluster_num in clusters:
            data.append({
                'x': [],
                'y': None,
                'name': 'Network: ' + str(cluster_num[1]),
                'type': 'bar'
            })
            
        last_cluster = -1
        last_paragraph = -1
        for occurrence_num, occurrence in enumerate(cluster_sequence):
            if occurrence[0] == last_paragraph: # two networks occurring in same paragraph
                continue
            if occurrence_num == len(cluster_sequence) -1: # last occurrence in list
                for i in range(last_paragraph+1, self.num_paragraphs()-1):
                    data[last_cluster]['x'].append(i)
            elif last_paragraph < occurrence[0]-1: # gap since last occurrence - fill
                for i in range(last_paragraph+1, occurrence[0]):
                    data[last_cluster]['x'].append(i)
                data[occurrence[1]]['x'].append(occurrence[0])
            else:
                data[occurrence[1]]['x'].append(occurrence[0])
            last_cluster = occurrence[1]
            last_paragraph = occurrence[0]
            
        max_network_size = 0
        
        for dat in data:
            max_network_size = max(max_network_size, len(dat['x']))
            
        y = []
        for i in range(max_network_size):
            y.append(1)
            
        colour_list = []
        for network_num, network in enumerate(clusters):
            if(len(cluster_colours) > network_num):
                colour_list.append(cluster_colours[network_num])
            else:
                colour_list.append('rgba('+str(randint(0, 255))+','+str(randint(0, 255))+','+str(randint(0, 255))+',1)')
            
        for dat_num, dat in enumerate(data):
            dat['y'] = y
            dat['marker'] = dict(color=colour_list[dat_num])
            dat['legendgroup'] = str(dat_num)
            
        layout = {
                'xaxis': {'title': 'Paragraph Number'},
                'yaxis': {'title': ''},
                'barmode': 'relative',
                'title': 'Network Occurrence Sequence'
            }
        
        plotly.offline.plot({'data': data, 'layout': layout}, filename=file_name)

    def network_sequence_repetition(self, entities, window, min_size):
        sequences = self.cooccurrence_jump_sequences(entities, window, min_size)
        sequences = [x[1] for x in sequences] # ignore when these repetitions occur, only which networks are involved
        start_length = 2
        rep_length = start_length
        reps = []
        while True:
            reps.append([])
            for seq_number, sequence in enumerate(sequences):
                if seq_number + rep_length  <= len(sequences): # enough sequences exist in the list
                    pattern = ''
                    for i in range(rep_length):
                        pattern += str(sequences[seq_number + i]) + ", "
                    pattern = pattern[:-2]
                    should_append = True
                    for rep in reps[rep_length - start_length]:
                        if rep[0] == pattern:
                            rep[1] += 1
                            should_append = False
                    if should_append:
                        reps[rep_length - start_length].append([pattern, 1])
                else:
                    break
            to_remove = []
            for rep in reps[rep_length - start_length]:
                if rep[1] == 1:
                    to_remove.append(rep)
            for rep in to_remove:
                reps[rep_length - start_length].remove(rep)
            if len(reps[rep_length - start_length]) == 0:
                reps.pop()
                break
            rep_length += 1
            
        '''for rep_set_num, rep_set in enumerate(reps):
            for rep in rep_set:
                for rep_set_num_2, rep_set_2 in enumerate(reps):
                    if rep_set_num_2 <= rep_set_num:
                        continue
                    for rep_2 in rep_set_2:
                        
                        if rep[0] in rep_2[0]:
                            rep[1] -= rep_2[1]
                        
        removals = []
        for set_num, rep_set in enumerate(reps):
            for rep in rep_set:
                if rep[1] == 0:
                    removals.append([set_num, rep])
        for removal in removals:
            reps[removal[0]].remove(removal[1])'''
            
        reps = [sorted(x, key=lambda x: x[1], reverse=True) for x in reversed(reps)]
        return reps
        
    def most_frequent_sequences(self, entities, window, min_size):
        for phrase in reversed(self.network_sequence_repetition(entities, window, min_size)):
            print(str(phrase[0][1]) + "\toccurrences of sequence <"+phrase[0][0]+">")
            if(len(phrase) > 1):
                print(str(phrase[1][1]) + "\toccurrences of sequence <"+phrase[1][0]+">")
            
        