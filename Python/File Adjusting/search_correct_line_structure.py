import nltk

line_no = 0
with open("Full Text.txt", "r") as file:
    for line in file:
        line_no += 1
        if line == "\n":
            continue
        tokens = nltk.word_tokenize(line)

        if len(tokens) >0:
            if len(tokens[0]) > 0:
                if not tokens[0][0] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    print ("ERROR 0 at "+str(line_no) +"\t" + line)
            last_word = tokens[len(tokens)-1]
            if len(last_word) > 0:
                if not last_word[len(last_word)-1] in ".?!":
                    print ("ERROR 1 at "+str(line_no))