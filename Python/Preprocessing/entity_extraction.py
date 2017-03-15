import nltk
import os.path

class Entities(object):
    entities = None # replacing awkward tree format with simple tuples
    single_entities = None # contains no duplicates with different tags
    textType = None

    def __init__(self, textType):
        self.entities = []
        self.textType = textType

    def extract_entities(self):
        ne_set = []
        file = open(self.textType+".txt", "r")
        text = file.read()
        file.close()
        paragraphs = text.split("\n\n")
        num_paragraphs =  float(len(paragraphs))
        last_percentage = -1 # for printing progress
        for paragraph_num, paragraph in enumerate(paragraphs):
            p_tokens = nltk.sent_tokenize(paragraph)
            for sentence in  p_tokens:
                s_tokens = nltk.word_tokenize(sentence)
                tagged = nltk.pos_tag(s_tokens)
                chunks = nltk.ne_chunk(tagged, binary=False)

                for chunk in chunks:
                    if type(chunk).__name__=="Tree":
                        if not chunk in ne_set:
                            ne_set.append(chunk)
            percentage = int((paragraph_num / num_paragraphs)*100)
            if percentage % 5 == 0 and percentage != last_percentage:
                last_percentage = percentage
                print(str(int((paragraph_num / num_paragraphs)*100)) + "%")

        for entity in ne_set:
            entity_string = ""
            for index, word in enumerate(entity):
                entity_string += str(entity[index][0]) + " "
            self.entities.append([str(entity.label()), entity_string])
        self.remove_exceptions()
        self.remove_duplicates()
        self.write_all_to_file()
        self.write_only_strings_to_file()

    def get_only_strings(self):
        output = []
        for entity in self.entities:
            if not entity[1] in output:
                output.append(entity[1])
        return output

    def remove_exceptions(self):
        exceptions = "Say,Italian,Clara Schumann,Ach,Pitcher,Long Ago,Poor Beethoven,Poor Aristotle,Mlle,Eglantine,Sam,Usual,Stan,Usual,Julius,Garbage Disposal Area,Maurice Utrillo,Aha,Sooner,Father,Frans,Ralph,Hodgson,German,Catholic,Faust Symphony,Lake,Como,Whereas,Simply,Jewish,Mexican,Gaetano,Music,Babe,Ruth,French,Katharine,Hepburn,Marlon,Brando,Wuthering,John Ruskin,Normally,John Everett Millais,Dutch,Too,Madness,Skirt,Sunlight,Baggage,Books,Russian,Chinese,Again,Little,Hereabouts,Ionian,Spartan,British,Halfway,Egyptian,Four Serious Songs,Brooke,Robert,Rodion Romanovitch Raskolnikov,Brook,Russell,Grass Was Real,Piero,Francesca,Steps,Arabia,Ferrier,Lucia,Pablo Picasso,Rodion Romanovitch Raskolnikov Mews,Sor Juana Ines de,Hugo,Goes,Cruz,Bertrand,Russel,Piero,Cosimo,Supper,Kirsten,Flagstad,Sculpture,Sistine,Seasons,Goes,Ludwig Wittgenstein,Guy,Anna,Karenina,Good,Origin,Trojan,Maupassant,Sister,Greek,English,Strauss,Levi,Franz,Schubert,Love,Song,Akhmatova,Unless,Great,Delft,Bronte,Bellini,Gilbert,Murray,Trojan Women,Greek,Juana Ines de,Carel,Fabritius,Max J.,Jacques,Oh,Washington,D.C.,Does,Which,Van,Gogh,Vincent,Vincent Van, Vincent Van Gogh,Never,St.,La,Hm,Doubtless,Well,Tate,Spanish,Eiffel,Four,Was,Imagine,Quite,Taddeo,Gaddi,Ludwig,Can,William,Anxiety,Sor,Gaddis,Rogier,Weyden,Antonio,Marco,Oca,Lucien,Nor,Rain,Down,Turner,John,Water,Marco,Dear,Kerosene,Certain,Thomas,Very,Knock,Sunshine,Months,Poor,High,Part,Leonardo,Vinci,Andrea,Sarto,Kathleen,Brahms I,Jackson,Pollock,Merciful,Tell,Suppose,Keeper,Ah,Saint,Brush,Damnation,Bay,Cassandra I,Andrei,Roublev,Doubtless A.,Housman,Clara,Jan,Steen,Rainer Maria,Alto,Martin,Heidegger,All Flesh,All Meat,Lawrence,Sor Juana Ines,Antonio Montes,Greco,Grass Is,Wrist,Willem,Kooning,Callas,Long Island Sound,Jane,Broken Bottles,Willem de Kooning,Jan Vermeer,Baseball,Peter,Metropolitan Museum"
        additions = [['PERSON', 'Rogier van der Weyden '],
                    ['PERSON', 'Andrea senza errori '],
                    ['PERSON', 'Andrea del Sarto '],
                    ['PERSON', 'A. E. Housman '],
                    ['PERSON', 'Lawrence of Arabia '],
                    ['PERSON', 'Guy de Maupassant '],
                    ['PERSON', 'de Kooning '],
                    ['PERSON', 'Max J. Friedlander '],
                    ['PERSON', 'Juana Ines '],
                    ['PERSON', 'Piero di Cosimo '],
                    ['PERSON', 'Hugo van der Goes '],
                    ['PERSON', 'Piero della Francesca '],
                    ['PERSON', 'Mlle. Eglantine '],
                    ['PERSON', 'Babe Ruth '],
                    ['GPE', 'Washington D.C. '],
                    ['GPE', 'Sistine Chapel ']]
        removals = []
        for entity in self.entities:
            if entity[1][:-1] in exceptions:
                removals.append(entity)
        for removal in removals:
            self.entities.remove(removal)
        self.entities.extend(additions)

    def remove_duplicates(self):
        output = []
        for entity in self.entities:
            broken = False
            for found in output:
                if entity[1] == found[1]:
                    broken = True
                    break
            if not broken:
                output.append(entity)
        self.single_entities = output
        
    def write_only_strings_to_file(self):
        filePath = "NE_Only_Strings_" + self.textType
        if os.path.exists(filePath + ".txt"):
            file_index = 0
            while os.path.exists(filePath + "_" + str(file_index) + ".txt"):
                file_index += 1
            filePath = filePath + "_" + str(file_index) + ".txt"
        else:
            filePath += ".txt"
        file = open(filePath, "w")
    
        entities = self.get_only_strings()
        for entity in entities:
            file.write(str(entity) + "\n")

        file.close()

    def write_all_to_file(self):
        filePath = "Named_Entities_" + self.textType
        if os.path.exists(filePath + ".txt"):
            file_index = 0
            while os.path.exists(filePath + "_" + str(file_index) + ".txt"):
                file_index += 1
            filePath = filePath + "_" + str(file_index) + ".txt"
        else:
            filePath += ".txt"
        file = open(filePath, "w")
    
        for entity in self.entities:
            file.write(str(entity) + "\n")

        file.close()

    def read_saved_entities(self, index = ""):
        url = "Named_Entities_" +self.textType+"_"+ str(index) +".txt" if (index != "") else "Named_Entities_" + self.textType +".txt"
        if os.path.exists(url):
            file = open(url, "r")
            text = file.read()
            file.close()
            phrases = []
            paragraphs = text.split("\n")
        
            for paragraph in paragraphs:
                if len(paragraph) < 5: #avoid messing with lines with no data
                    continue
                paragraph = paragraph[2:-2]
                
                new_entity = paragraph.split("', '")
                if len(new_entity) < 2:
                    new_entity = paragraph.split("', \"")
                
                self.entities.append(new_entity)
            #print(self.entities)

        else:
            print("File not found")






