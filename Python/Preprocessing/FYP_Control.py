import entity_extraction
import phrases
import nltk
import plotly

textType = "Full"
#textType = "Single"

unique = True

phrases = phrases.Phrases(textType, 3)
phrases.read_saved_phrases(0)

#phrases.read_text(['.', ','])
#phrases.read_text_old(['.', ','], unique)

entities = entity_extraction.Entities(textType)
#entities.extract_entities()
entities.read_saved_entities()

#phrases.write_to_csv()

#phrases_with_nes = phrases.phrases_with_entities(entities)

'''occurrence_tuples = phrases.entity_occurrence_in_phrases_tuples(entities)
for tuple in occurrence_tuples:
    print(tuple)'''
'''cooccurrences = phrases.cooccurrences(entities, 1)
for co in cooccurrences:
    print (co);'''

#phrases.write_to_gephi_file(entities, 0)
#phrases.write_to_gephi_file(entities, 1)


#for phrase in phrases.phrases[len(phrases.phrases)-1]:
#    print(phrase)

#phrases.network_sequence_graph(entities, 0, 3, "network_sequences.html")

phrases.most_frequent_sequences(entities, 0, 3)