import enchant
import nltk

d = enchant.Dict("en_US")
data = ""
line_no = 0
tracked = []
output = []

with open("Full Text.txt", "r") as file:
    for line in file:
        line_no += 1
        tokens = nltk.word_tokenize(line)
        token_set = set(tokens)
        token_set = sorted(token_set)

        for i in range(len(token_set)):
            curr = token_set.pop()
            
            if not curr in tracked:
                
                if not d.check(curr):
                    tracked.append(curr)
                    output.append([curr, line_no])

sorted = sorted(output)
for occurance in sorted:
    print (occurance)